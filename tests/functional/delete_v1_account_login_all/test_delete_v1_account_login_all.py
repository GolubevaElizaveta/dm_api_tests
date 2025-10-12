import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login/all")
@allure.sub_suite("Позитивные тесты")
@allure.title("Проверка разлогина текущего пользователя со всех устройств")

def test_delete_v1_account_login_all(auth_account_helper):
    auth_account_helper.dm_account_api.login_api.delete_v1_account_login_all()