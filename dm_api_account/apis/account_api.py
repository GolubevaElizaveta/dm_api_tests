import requests

from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data
    ):
        """"
        Register new user
        :param json_data
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_email(
            self,
            json_data
    ):
        """
        Change user's email
        :param json_data:
        :return:
        """
        response = self.put(
            path=f'/v1/account/email',
            json=json_data
        )
        return response

    def get_v1_account(
            self,
            **kwargs
    ):
        """"
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        return response

    def post_v1_account_password(
            self,
            json_data,
            **kwargs
    ):
        """
        Reset registered user password
        :param
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            **kwargs,
            json = json_data
        )
        return response

    def put_v1_account_password(
            self,
            json_data,
            **kwargs
            ):
        response = self.put(
            path=f'/v1/account/password',
            **kwargs,
            json=json_data)
        return response
