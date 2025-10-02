import allure

from checkers.http_checkers import check_status_code_http

import pytest

from checkers.post_v1_account import PostV1Account

@allure.suite("Тесты на проверку метода POST v1/account")
@allure.sub_suite("Позитивные тесты")
class TestsPostV1Account:
    @allure.title("Проверка регистрации нового пользователя")
    def test_post_v1_account(self,account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1Account.check_response_values(response)


@pytest.mark.parametrize(
    "login, email, password, expected_status_code, expected_message, expected_errors",
    [
        ("egolubeva", "egolubeva@mail.ru", "123", 400, "Validation failed", {"Password": ["Short"]}),
        ("egolubeva", "egolubevamail.ru", "123456789", 400, "Validation failed", {"Email": ["Invalid"]}),
        ("e", "egolubeva@mail.ru", "123456789", 400, "Validation failed", {"Login": ["Short"]}),
    ]
)
@allure.title("Проверка обработки неверных значений параметров")
def test_post_v1_account_negative(account_helper, login, email, password, expected_status_code, expected_message, expected_errors):
    with check_status_code_http(
        expected_status_code=expected_status_code,
        expected_message=expected_message,
        expected_errors=expected_errors
    ):
        account_helper.register_new_user(
            login=login,
            email=email,
            password=password
        )