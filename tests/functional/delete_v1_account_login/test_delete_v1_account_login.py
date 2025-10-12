import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login")
@allure.sub_suite("Позитивные тесты")
@allure.title("Проверка разлогина текущего пользователя")

def test_delete_v1_account_login(auth_account_helper):
    auth_account_helper.dm_account_api.login_api.delete_v1_account_login()