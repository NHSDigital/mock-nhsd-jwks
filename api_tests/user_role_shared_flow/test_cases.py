import json
import pytest
import requests
from assertpy import assert_that
from api_tests.config_files import config
from api_test_utils.oauth_helper import OauthHelper
from api_test_utils.apigee_api_apps import ApigeeApiDeveloperApps


@pytest.mark.asyncio
class TestCasesSuite:
    """ A test suite for the user role service shared flow """

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
    async def test_happy_path(self, test_app):
        oauth = OauthHelper(
            client_id=test_app.client_id,
            client_secret=test_app.client_secret,
            redirect_uri=test_app.callback_url,
        )
        token = await oauth.get_token_response(grant_type="authorization_code")
        token = token["body"]["access_token"]
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.USER_ROLE_SHARED_FLOW,
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Session-URID": "555254242102",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.asyncio
    async def test_default_role(self, test_app):
        oauth = OauthHelper(
            client_id=test_app.client_id,
            client_secret=test_app.client_secret,
            redirect_uri=test_app.callback_url,
        )
        token = await oauth.get_token_response(grant_type="authorization_code")
        token = token["body"]["access_token"]
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.USER_ROLE_SHARED_FLOW,
            headers={"Authorization": f"Bearer {token}"},
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.asyncio
    async def test_user_invalid_role_in_header(self, test_app):
        oauth = OauthHelper(
            client_id=test_app.client_id,
            client_secret=test_app.client_secret,
            redirect_uri=test_app.callback_url,
        )
        token = await oauth.get_token_response(grant_type="authorization_code")
        token = token["body"]["access_token"]
        # Given
        expected_status_code = 401

        # When
        response = requests.get(
            url=config.USER_ROLE_SHARED_FLOW,
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Session-URID": "notAuserRole123",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.asyncio
    async def test_missing_role_token(self, test_app):
        oauth = OauthHelper(
            client_id=test_app.client_id,
            client_secret=test_app.client_secret,
            redirect_uri=test_app.callback_url,
        )
        jwt = oauth.create_jwt(kid="test-1")
        token = await oauth.get_token_response(
            grant_type="client_credentials", _jwt=jwt
        )
        token = token["body"]["access_token"]
        # Given
        expected_status_code = 401

        # When
        response = requests.get(
            url=config.USER_ROLE_SHARED_FLOW,
            headers={"Authorization": f"Bearer {token}"},
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
