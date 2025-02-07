from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from json import loads
from retrying import retry
import time

def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None

# def retrier(function):
#     def wrapper(*args, **kwargs):
#         token = None
#         count = 0
#         while token is None:
#             print(f"Попытка получения токена номер {count}")
#             token=function(*args, **kwargs)
#             count += 1
#             if count == 5:
#                 raise AssertionError("Превышено количество попыток получения активационного токена")
#             if token:
#                 return token
#             print(f"Попытка получения токена номер {count}")
#             time.sleep(1)
#     return wrapper

class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(self, login: str, password: str, email: str, max_attempts: int = 5):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не был создан, {response.json()}"
        token= self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login}, не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"
        return response

    def user_login(
                self,
                login: str,
                password: str,
                remember_me: bool = True
        ):
            json_data = {
                'login': login,
                'password': password,
                'rememberMe': remember_me,
            }
            response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
            assert response.status_code == 200, "Пользователь не был авторизован"
            return response

    def update_user_email(
            self,
            login: str,
            password: str,
            new_email: str
            ):
        # Смена email
        json_data = {
            'login': login,
            'password': password,
            'email': new_email,
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, "Email не был изменен"
        # Попытка войти после смены почты
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, "Вход пользователя не был запрещен"
        token = self.get_activation_token_by_email(email=new_email)
        assert token is not None, f'Токен для новой почты {new_email} пользователя {login} не был получен'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"

    @retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_result=retry_if_result_none)
    def get_activation_token_by_login(self,login):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data.get('Login')
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token

    @retry(stop_max_attempt_number=5, wait_fixed=1000, retry_on_result=retry_if_result_none)
    def get_activation_token_by_email(
            self,
            email
            ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_email = item['Content']['Headers']['To'][0]
            if user_email == email:
                user_data = loads(item['Content']['Body'])
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                break
        return token