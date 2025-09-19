
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    has_properties,
    has_items,
    greater_than_or_equal_to
)

def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
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
    print(response)



def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)