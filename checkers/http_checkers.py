# from contextlib import contextmanager
# import requests
# from requests.exceptions import HTTPError
#
# @contextmanager
# def check_status_code_http(expected_status_code=requests.codes.OK,
#                            expected_message: str = "", expected_errors: dict = None):
#     try:
#         yield
#         if expected_status_code != requests.codes.OK:
#             raise AssertionError(f"Ожидаемый статус код должен быть равен {expected_status_code}")
#         if expected_message:
#             raise AssertionError(f"Должно быть получено сообщение '{expected_message}', но запрос прошел успешно")
#         if expected_errors:
#             raise AssertionError(f"Должны быть получены ошибки '{expected_errors}', но запрос прошел успешно")
#     except HTTPError as e:
#         # print("Отладочная информация:", e.response.json())
#         actual_status_code = e.response.status_code
#         actual_message = e.response.json().get('title', '')
#         actual_errors = e.response.json().get('errors', {})
#
#         assert actual_status_code == expected_status_code, f"Ожидался статус код {expected_status_code}, а получили {actual_status_code}"
#         assert actual_message == expected_message, f"Ожидалось сообщение '{expected_message}', а получили '{actual_message}'"
#         if expected_errors:
#             assert actual_errors == expected_errors, f"Ожидалась ошибка '{expected_errors}', а получили '{actual_errors}'"

import allure
from contextlib import contextmanager
import requests
from requests.exceptions import HTTPError

@contextmanager
def check_status_code_http(expected_status_code=requests.codes.OK,
                           expected_message: str = "", expected_errors: dict = None):
    with allure.step("Начало проверки статуса HTTP-кода"):
        try:
            yield
            with allure.step(f"Проверка успешного выполнения: ожидаемый код {expected_status_code}"):
                if expected_status_code != requests.codes.OK:
                    raise AssertionError(f"Ожидаемый статус код должен быть равен {expected_status_code}")
                if expected_message:
                    raise AssertionError(f"Должно быть получено сообщение '{expected_message}', но запрос прошел успешно")
                if expected_errors:
                    raise AssertionError(f"Должны быть получены ошибки '{expected_errors}', но запрос прошел успешно")
        except HTTPError as e:
            # print("Отладочная информация:", e.response.json())
            actual_status_code = e.response.status_code
            actual_message = e.response.json().get('title', '')
            actual_errors = e.response.json().get('errors', {})

            with allure.step(f"Проверка кода ошибки: ожидаемый {expected_status_code}, фактический {actual_status_code}"):
                assert actual_status_code == expected_status_code, f"Ожидался статус код {expected_status_code}, а получили {actual_status_code}"
            with allure.step(f"Проверка сообщения об ошибке: ожидаемое '{expected_message}', фактическое '{actual_message}'"):
                assert actual_message == expected_message, f"Ожидалось сообщение '{expected_message}', а получили '{actual_message}'"
            if expected_errors:
                with allure.step(f"Проверка ошибок: ожидаемые {expected_errors}, фактические {actual_errors}"):
                    assert actual_errors == expected_errors, f"Ожидалась ошибка '{expected_errors}', а получили '{actual_errors}'"