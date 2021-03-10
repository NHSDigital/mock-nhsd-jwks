import json
import pytest
import requests
from assertpy import assert_that
from api_tests.config_files import config

@pytest.mark.usefixtures("setup")
class TestCasesSuite:
    """ A test suite for the user role service shared flow """

    @pytest.mark.usefixtures('get_token_internal_dev')
    def test_happy_path(self):
        # Given
        expected_status_code = 404

        # When
        response = requests.get(
            url=config.USER_ROLE_SHARED_FLOW,
            headers={
                'Authorization': f'Bearer {self.token}',       
                'user_role': '555254242102'                         
            }
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
