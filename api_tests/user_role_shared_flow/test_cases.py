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
        expected_response = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImlkZW50aXR5LXNlcnZpY2UtdGVzdHMtMSJ9.eyJhdF9oYXNoIjoidGZfLWxxcHEzNmx3TzdXbVNCSUo2USIsInN1YiI6Ijc4NzgwNzQyOTUxMSIsImF1ZGl0VHJhY2tpbmdJZCI6IjkxZjY5NGU2LTM3NDktNDJmZC05MGIwLWMzMTM0YjBkOThmNi0xNTQ2MzkxIiwiYW1yIjpbIk4zX1NNQVJUQ0FSRCJdLCJpc3MiOiJodHRwczovL2FtLm5oc2ludC5hdXRoLXB0bC5jaXMyLnNwaW5lc2VydmljZXMubmhzLnVrOjQ0My9vcGVuYW0vb2F1dGgyL3JlYWxtcy9yb290L3JlYWxtcy9OSFNJZGVudGl0eS9yZWFsbXMvSGVhbHRoY2FyZSIsInRva2VuTmFtZSI6ImlkX3Rva2VuIiwiYXVkIjoic29tZS1jbGllbnQtaWQiLCJjX2hhc2giOiJiYzd6ekdrQ2xDM01FaUZRM1loUEtnIiwiYWNyIjoiQUFMM19BTlkiLCJvcmcuZm9yZ2Vyb2NrLm9wZW5pZGNvbm5lY3Qub3BzIjoiLUk0NU5qbU1EZE1hLWFORjJzcjloQzdxRUdRIiwic19oYXNoIjoiTFBKTnVsLXdvdzRtNkRzcXhibmluZyIsImF6cCI6InNvbWUtY2xpZW50LWlkIiwiYXV0aF90aW1lIjoxNjEwNTU5ODAyLCJyZWFsbSI6Ii9OSFNJZGVudGl0eS9IZWFsdGhjYXJlIiwiZXhwIjoxNjgxODY1Nzg1LCJ0b2tlblR5cGUiOiJKV1RUb2tlbiIsImlhdCI6MTYyMTg2NTc3NSwic2VsZWN0ZWRfcm9sZWlkIjoiNTU1MjU0MjQyMTAyIn0.UVVozQz5fJDqzRta3NsbbJ6tldbFKtnPwrUHvDtGKGGYGEm1Bx1mY9QubB2HpX6yJT_dN5VGbFf-dsiqk7WV0wGXxfA3vabSf-OF68hEwed291_bmLOSkUrHbf5tLYFWAAqri3F-TzWhGGknBQ6FfttXpDeRtLodf03-jX-KeFomL_4ofLYjugiRD636Jjzt7_RdRmyaRL-sKMfIoabW6wsNO-ifAJrhyGIqRuLZB_HJuZgiHOAlLIHejJgJkvpfmsn-hPbkKKM21h4mc73WlHMISp0B07vRFYj1IXhkcE2zpRnM33eLFJqrTyWZhl5LNb6J-yI-2GnykYpqKIyvww"

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

    @pytest.mark.asyncio
    async def test_nhs_login_simulated_token_response(self):
        # Given
        expected_status_code = 200
        # This long term id_token expiries on 2023. We will implement a full OIDC provider before that.
        expected_response = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiIsImtpZCI6Im5ocy1sb2dpbiIsInN1YiI6IjQ5ZjQ3MGExLWNjNTItNDliNy1iZWJhLTBmOWNlYzkzN2M0NiIsImF1ZCI6IkFQSU0tMSIsImlzcyI6Imh0dHBzOi8vaW50ZXJuYWwtZGV2LmFwaS5zZXJ2aWNlLm5ocy51ayIsImV4cCI6MTYxNjYwNDU3NCwiaWF0IjoxNjE2NjAwOTc0LCJqdGkiOiJiNjhkZGIyOC1lNDQwLTQ0M2QtODcyNS1kZmUwZGEzMzAxMTgifQ.eyJhdWQiOiJzb21lLWNsaWVudC1pZCIsImlkX3N0YXR1cyI6InZlcmlmaWVkIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MTY2MDA2ODMsImlzcyI6Imh0dHBzOi8vaW50ZXJuYWwtZGV2LmFwaS5zZXJ2aWNlLm5ocy51ayIsInZvdCI6IlA5LkNwLkNkIiwiZXhwIjoxNjgzMzMxMTY2LCJpYXQiOjE2MjMzMzExNTYsInZ0bSI6Imh0dHBzOi8vYXV0aC5zYW5kcGl0LnNpZ25pbi5uaHMudWsvdHJ1c3RtYXJrL2F1dGguc2FuZHBpdC5zaWduaW4ubmhzLnVrIiwianRpIjoiYjY4ZGRiMjgtZTQ0MC00NDNkLTg3MjUtZGZlMGRhMzMwMTE4IiwiaWRlbnRpdHlfcHJvb2ZpbmdfbGV2ZWwiOiJQOSJ9.jEOMCrD5n05KZFG2NSdBC9ENvaX8Hw8PhLB0ZIUR_0Ibz2j5lUUpi-f6imBNGYEkci9XtekfKYQrQn3s2V6BmFzv_XhhPWHjNabEaBsZOScRHXCp5KaU0WSeRts5ldcXfQvSmz_CEA7MPUZSxqUjw_4Yc7HdN9ocnwCBaCwCiLXkxlHeeajfYJXAfzdNd9iLK9HUZxojw_mHkb11CiNb0JHWKtMfghVK0OsvK-N0xsMAurqKwbhSJecteJm13GOfwpBCj9oWQYhalDhVXT12IfGXynEuhh8IUkvjHpgwUdVwMpx-zdraiRubZZ1X5W4Bc1wf1zl3xp2BgjVKAhOK-v-eekyXHxmv923ErTg2Fd3_A5U9_0i2CJJ3ICg1jHdfyVslntiavR5mM7OlPUlWAU6i1SdWkijLDtv_5jAnILZdd-cT2X0R_hJ-CwokbfQy_w180NzW8sqKI0Aw8LXiqStuh7dks77JKOrbS1drnJ0JzN8cyJTPA7mZgby9uDwmblOVY5AT65y5Y_Tc-qFd6b_3aSszVfEDKAsMG7jyLOIJnsmemiDSPdJes0m2xn9plnn_xrrWoP6XA5vONfGwP-aLinfd8wAhNRCIvjMqcMeu8zDZpRayhKY7iVzk5UQPvK20ha__pjemeVD9FfeB3iC0bPG7DSWc4RmfQwXyzF4"

        # When
        response = requests.post(
            url=config.MOCK_PROXY_BASE_PATH + '/nhs_login_simulated_token'
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_response).is_equal_to(response.json()['id_token'])