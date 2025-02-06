from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from json import loads
from json import JSONDecodeError

class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):

        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, "Пользователь не был создан"
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        token = self.get_activation_token_by_login(login, response)
        assert token is not None, f"токен для пользователя {login}, не был получен"
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

    @staticmethod
    def get_activation_token_by_login(login, response):
        token = None
        for item in response.json().get('items', []):
            try:
                # Предполагаем, что формат в JSON, но может быть и текст
                user_data = loads(item['Content']['Body'])
                user_login = user_data.get('Login')
                if user_login == login:
                    token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                    break
            except (JSONDecodeError, KeyError):
                # Если не удается декодировать JSON или отсутствует ключ, переходим к следующему элементу
                continue
        return token