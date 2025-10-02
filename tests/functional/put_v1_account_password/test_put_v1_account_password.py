import allure


@allure.suite("Тесты на проверку метода PUT v1/account/password")
@allure.sub_suite("Позитивные тесты")
@allure.title("Проверка смены пароля пользователя")
def test_put_v1_account_password(
        account_helper,
        prepare_user,
        ):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = f'{password}_new'
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_password(login=login, email=email, old_password=password, new_password=new_password)
    account_helper.user_login(login=login, password=new_password)
