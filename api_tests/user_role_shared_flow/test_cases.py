import json
import pytest
import requests
from assertpy import assert_that
from api_tests.config_files import config
from api_test_utils.oauth_helper import OauthHelper
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps


@pytest.mark.asyncio
class TestCasesSuite:
    """ A test suite for the mock oidc responses """

    @pytest.fixture()
    async def test_app(self):
        """Testing App Setup"""
        apigee_app = ApigeeApiDeveloperApps()
        print("Creating Test App..")
        await apigee_app.create_new_app(
            callback_url="https://nhsd-apim-testing-internal-dev.herokuapp.com/callback"
        )

        # Set default JWT Testing resource url
        await apigee_app.set_custom_attributes(
            {
                "jwks-resource-url": "https://raw.githubusercontent.com/NHSDigital/"
                "identity-service-jwks/main/jwks/internal-dev/"
                "9baed6f4-1361-4a8e-8531-1f8426e3aba8.json"
            }
        )

        await apigee_app.add_api_product(api_products=[config.MOCK_PROXY_PATH])

        yield apigee_app
        print("Destroying Test App..")
        await apigee_app.destroy_app()

    @pytest.mark.asyncio
    async def test_cis2_simulated_token_response(self):
        # Given
        expected_status_code = 200
        # This long term id_token expiries on 2023. We will implement a full OIDC provider before that.
        expected_response = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImlkZW50aXR5LXNlcnZpY2UtdGVzdHMtMSJ9.eyJhdF9oYXNoIjoidGZfLWxxcHEzNmx3TzdXbVNCSUo2USIsInN1YiI6Ijc4NzgwNzQyOTUxMSIsImF1ZGl0VHJhY2tpbmdJZCI6IjkxZjY5NGU2LTM3NDktNDJmZC05MGIwLWMzMTM0YjBkOThmNi0xNTQ2MzkxIiwiYW1yIjpbIk4zX1NNQVJUQ0FSRCJdLCJpc3MiOiJodHRwczovL2FtLm5oc2ludC5hdXRoLXB0bC5jaXMyLnNwaW5lc2VydmljZXMubmhzLnVrOjQ0My9vcGVuYW0vb2F1dGgyL3JlYWxtcy9yb290L3JlYWxtcy9OSFNJZGVudGl0eS9yZWFsbXMvSGVhbHRoY2FyZSIsInRva2VuTmFtZSI6ImlkX3Rva2VuIiwiYXVkIjoic29tZS1jbGllbnQtaWQiLCJjX2hhc2giOiJiYzd6ekdrQ2xDM01FaUZRM1loUEtnIiwiYWNyIjoiQUFMM19BTlkiLCJvcmcuZm9yZ2Vyb2NrLm9wZW5pZGNvbm5lY3Qub3BzIjoiLUk0NU5qbU1EZE1hLWFORjJzcjloQzdxRUdRIiwic19oYXNoIjoiTFBKTnVsLXdvdzRtNkRzcXhibmluZyIsImF6cCI6InNvbWUtY2xpZW50LWlkIiwiYXV0aF90aW1lIjoxNjEwNTU5ODAyLCJyZWFsbSI6Ii9OSFNJZGVudGl0eS9IZWFsdGhjYXJlIiwiZXhwIjoxNjgwOTA4MDUwLCJ0b2tlblR5cGUiOiJKV1RUb2tlbiIsImlhdCI6MTYyMDkwNzk1MH0.nbwUyF2c3ab56cv6WLx4BvLzgGM7RUHrgSagefBPTjgR0lkTZz_84RsMS7FQs1eOYcP5WIMumgcxZELqyduCRxaeJmVCfoEnjfX2lzkl2mPZjsalrKTFGjUk3VQxYxlzX1ifznzMekoBGeFjtP7Eb3mhkaJH3ibTDTGLIvHejgeIeO34-2eq_Q6fktbw0cWgmgpPFZ-E62WQGZVjKht4DruRDF1GrqgyolGG8RdPIvyvYCJBq5v6kPLz-CkKH_SusgKkTam2DKvRj566Qob3NlHm9KNkh_4cE8NAUudtgNpZCTB_jogArB51SfwRB6Xb6rJ3NDBh2QuSwrTDW1v2XA"

        # When
        response = requests.post(
            url=config.MOCK_PROXY_BASE_PATH + '/cis2_simulated_token'
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_response).is_equal_to(response.json()['id_token'])

    @pytest.mark.asyncio
    async def test_cis2_public_key_response(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.MOCK_PROXY_BASE_PATH + '/identity-service/jwks'
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.asyncio
    async def test_nhs_login_public_key_response(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.MOCK_PROXY_BASE_PATH + '/identity-service/nhs-login-jwks'
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
