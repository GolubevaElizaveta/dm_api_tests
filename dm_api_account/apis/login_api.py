import requests
from restclient.client import RestClient

class LoginApi(RestClient):

    def post_v1_account_login(
            self,
            json_data
    ):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account/login',
            json=json_data
        )
        return response

    def delete_v1_account_login(
            self,
            **kwargs
    ):
        """
        Logout as current user
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login',
            **kwargs
        )
        return response

    def delete_v1_account_login_all(
            self,
            **kwargs
    ):
        """
        Logout from every device
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login/all',
            **kwargs
        )
        return response