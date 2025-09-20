from checkers.http_checkers import check_status_code_http
from dm_api_account.models.login_credentials import LoginCredentials

def test_put_v1_account_email(account_helper, prepare_user, remember_me=True):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = f'{email}_new'
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.update_user_email(login=login, password=password, new_email=new_email)

    login_credentials = LoginCredentials(
        login=login,
        password=password,
        remember_me=remember_me
    )

    with check_status_code_http(
            expected_status_code=403,
            expected_message="User is inactive. Address the technical support for more details"
    ):
        account_helper.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials,
            validate_response=False
        )

    token = account_helper.get_token(identifier=login, token_type="activation",identifier_type="login" )
    assert token is not None, f"Токен для пользователя {login} не был получен"
    account_helper.activate_user(token=token)
    account_helper.user_login(login=login, password=password)
