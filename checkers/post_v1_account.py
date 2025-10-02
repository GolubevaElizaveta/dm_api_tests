from datetime import datetime

import allure
from hamcrest import (
    assert_that,
    all_of,
    has_property,
    instance_of,
    starts_with,
    has_properties,
    equal_to,
)


class PostV1Account:
    @classmethod
    def check_response_values(cls, response):
        with allure.step("Проверка ответа"):
            today = datetime.now().strftime('%Y-%m-%d')
            assert_that(str(response.resource.registration), starts_with(today))

            assert_that(
                response, all_of(
                    has_property('resource', has_property('login', starts_with("egolubeva"))),
                    has_property('resource', has_property('registration', instance_of(datetime))),
                    has_property(
                        'resource', has_property(
                            'rating', has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                }
                            )
                        )
                    )
                )
            )

