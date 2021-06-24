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
        expected_response = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiIsImtpZCI6ImFjMTAyOWQyY2I4MWI0NTI3YTBiNjNlMmI0ZjI4MDM0NWYwNGRkNDIiLCJzdWIiOiI0OWY0NzBhMS1jYzUyLTQ5YjctYmViYS0wZjljZWM5MzdjNDYiLCJhdWQiOiJzb21lLWNsaWVudC1pZCIsImlzcyI6Imh0dHBzOi8vaW50ZXJuYWwtZGV2LmFwaS5zZXJ2aWNlLm5ocy51ayIsImV4cCI6MTY4MzMzMTE2NiwiaWF0IjoxNjIzODQ5MjcxLCJqdGkiOiI4ZWRhYmUyYi1jN2ZmLTQwYmQtYmM3Zi0wYjhkYzZhNTI0MjMifQ.eyJzdWIiOiI0OWY0NzBhMS1jYzUyLTQ5YjctYmViYS0wZjljZWM5MzdjNDYiLCJiaXJ0aGRhdGUiOiIxOTY4LTAyLTEyIiwibmhzX251bWJlciI6Ijk5MTIwMDMwNzEiLCJpc3MiOiJodHRwczovL2ludGVybmFsLWRldi5hcGkuc2VydmljZS5uaHMudWsiLCJ2dG0iOiJodHRwczovL2F1dGguc2FuZHBpdC5zaWduaW4ubmhzLnVrL3RydXN0bWFyay9hdXRoLnNhbmRwaXQuc2lnbmluLm5ocy51ayIsImF1ZCI6InNvbWUtY2xpZW50LWlkIiwiaWRfc3RhdHVzIjoidmVyaWZpZWQiLCJ0b2tlbl91c2UiOiJpZCIsInN1cm5hbWUiOiJNSUxMQVIiLCJhdXRoX3RpbWUiOjE2MjM4NDkyMDEsInZvdCI6IlA5LkNwLkNkIiwiaWRlbnRpdHlfcHJvb2ZpbmdfbGV2ZWwiOiJQOSIsImV4cCI6MTY4MzMzMTE2NiwiaWF0IjoxNjIzODQ5MjcxLCJmYW1pbHlfbmFtZSI6Ik1JTExBUiIsImp0aSI6IjhlZGFiZTJiLWM3ZmYtNDBiZC1iYzdmLTBiOGRjNmE1MjQyMyJ9.D4H6t8bne0I1kQvFSeLMkl7ITozyJd5tpJREKP3niiHlqgI1GXZVU3DJJW_p4ULkGBFPw302w56_f_hpAczNXDSWur0neF0KHdIhfFZwtrCrQ9CPvoal4tJLO5juHJorOndWSmtBeePBOx-Lf-nW55Rhsc5RMFcFX1SkkAxVKTG9aIFP0bH-2bcuOga1NbqZObm10_vYVJ23_y1cKvvpvacJ2WJY6W3Ei7YI3u3Wk7IJ9RPWAUZ2EhMGHiuZrnkdKdYNgVAbPekQatrJ4Wl8JC_1ulWIbrWHG7xc_UVMDsoZnxkshahqubifJYmZbKGohWurD1OqmD0DfCHTkZalH_B7SHSuI-3dt_Vzv3CK523ThVn5v_6OkJKO8lYUN8ldBaiCSpLai-BNfJT_p30_SQxm-bxIGKJVW_6kak7DJ3wbjkQasuZynsXmNWRR9yWqsAHdCed0rGTUalyjfHD3VJKMioC70_LqAnP6WRBOifmAnMybT3J99dth8xdPMxMZoiUMyVz6pt8w8KSnEcNOPkFFEOrL4Xge4dn7JHilS5TjhXDN2OmIbMUVtHQ69r1kT-5x1ABat6eOsI_DSUYtBAmZ61unj53mxr82QZeemPr5as9zlJY0nwDsdG9d4tfagDCOp8yAyHCmp5ZzAxgy_6KrUKAsu09zbmTwzuVe05o"

        # When
        response = requests.post(
            url=config.MOCK_PROXY_BASE_PATH + '/nhs_login_simulated_token'
        )

         # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_response).is_equal_to(response.json()['id_token'])
        
    @pytest.mark.asyncio
    async def test_userinfo_response(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.MOCK_PROXY_BASE_PATH + '/userinfo'
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(response.json()).is_not_equal_to({})