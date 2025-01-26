from json import loads
from json import JSONDecodeError
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi



def test_post_v1_account():
    # Регистрация пользователя
    account_api = AccountApi(host="http://5.63.153.31:5051")
    login_api = LoginApi(host="http://5.63.153.31:5051")
    mailhog_api = MailhogApi(host="http://5.63.153.31:5025")

    login = 'egolubeva_test12'
    email = f'{login}@mail.ru'
    password = '1234567891'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"токен для пользователя {login}, не был получен"

    # Активировать пользователя
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    # Меняем email
    new_email = "new_email103@mail.ru"
    json_data = {
        "login": login,
        "password": password,
        "email": new_email
    }
    response = account_api.put_v1_account_email(json_data=json_data)
    print(response.status_code)
    assert response.status_code == 200, "Не удалось изменить email"

    # Логинимся с новым email
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    assert response.status_code == 403, "Пользователь с данным email неактивен"


    # Получаем email для подтверждения смены
    response = mailhog_api.get_api_v2_messages()
    old_token = get_activation_token_by_login(login, response)
    new_token = get_activation_token_by_login(new_email, response)

    # Предполагая, что у нас есть старый токен, сохраненный в переменной old_token
    assert new_token != old_token, f"Нет подтверждения смены email для {new_email}. Токен не изменился."

    # Активируем новый email
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    assert response.status_code == 200, "Новый email не был активирован"

    # Логинимся с новым email
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

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
