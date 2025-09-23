from datetime import datetime

from hamcrest import (
    assert_that,
    all_of,
    has_property,
    starts_with,
    has_properties,
    has_items,
    greater_than_or_equal_to,
)

class GetV1Account:

    @classmethod
    def check_response_get_v1_account(cls, response):
        assert_that(
            response, all_of(
                has_property(
                    'resource', has_properties(
                        {
                            'login': starts_with("egolubeva"),
                            'roles': has_items("Guest", "Player"),
                            'rating': has_properties(
                                {
                                    "quality": greater_than_or_equal_to(0),
                                    "quantity": greater_than_or_equal_to(0)
                                }
                            )
                        }
                    )
                )
            )
        )