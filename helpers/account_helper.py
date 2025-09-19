from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from json import loads
from retrying import retry
import time

def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None

class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str,
    ):
        response = self.user_login(login=login, password=password)
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_new_user(self, login: str, password: str, email: str, max_attempts: int = 5):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был создан, {response.json()}"
        start_time=time.time()
        token= self.get_token(identifier=login, token_type="activation", identifier_type="login")
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        assert token is not None, f"Токен для пользователя {login}, не был получен"
        response = self.activate_user(token=token)
        return response

    def activate_user(
            self,
            token: str
            ):
        response = self.dm_account_api.account_api.put_v1_account_token(
            token=token
        )
        return response

    def user_login(
                self,
                login: str,
                password: str,
                remember_me: bool = True,
                validate_response=False,
                validate_headers=False
        ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=validate_response
            )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
            assert response.status_code == 200, "Пользователь не был авторизован"
        return response

    def update_user_email(
            self,
            login: str,
            password: str,
            new_email: str
            ):
        # Смена email
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=new_email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        return response
        # assert response.status_code == 200, "Email не был изменен"
        # # Попытка войти после смены почты
        # response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        # assert response.status_code == 403, "Вход пользователя не был запрещен"
        # token = self.get_token(identifier=new_email, token_type="activation", identifier_type="email")
        # assert token is not None, f'Токен для новой почты {new_email} пользователя {login} не был получен'
        # response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        # assert response.status_code == 200, "Пользователь не был активирован"

    @retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_result=retry_if_result_none)
    def get_token(
            self,
            identifier: str,
            token_type: str = "activation",
            limit: int = 20,
            identifier_type: str = "login"
            ):
        """
        Получение токена активации или сброса пароля.

        Args:
            identifier: логин или email пользователя.
            token_type: тип токена (activation или reset).
            limit: количество сообщений для проверки.
            identifier_type: тип идентификатора ("login" или "email").

        Returns:
            токен активации или сброса пароля.
        """
        # token = None
        params = {
            'limit': limit
        }
        response = self.mailhog.mailhog_api.get_api_v2_messages()

        token_name = "ConfirmationLinkUrl" if token_type.lower() == "activation" else "ConfirmationLinkUri"

        for item in response.json()["items"]:
            user_data = loads(item['Content']['Body'])
            if identifier_type == "login":
                user_identifier = user_data.get("Login")
            else:  # "email"
                user_identifier = item['Content']['Headers']['To'][0]

            if user_identifier == identifier:
                confirmation_link = user_data.get(token_name)
                if confirmation_link:
                    token = confirmation_link.split('/')[-1]
                    break
        return token

    def change_password(self, login: str, email: str, old_password: str, new_password: str):
        token = self.user_login(login=login, password=old_password)
        self.dm_account_api.account_api.post_v1_account_password(
            reset_password=ResetPassword (
                login=login,
                email=email
            ),
            headers={
                "x-dm-auth-token": token.headers["x-dm-auth-token"]
            },
        )
        token = self.get_token(identifier=login,token_type="reset", identifier_type="login")
        self.dm_account_api.account_api.put_v1_account_password(
            change_password=ChangePassword(
                login=login,
                token=token,
                old_password=old_password,
                new_password=new_password
            )
        )