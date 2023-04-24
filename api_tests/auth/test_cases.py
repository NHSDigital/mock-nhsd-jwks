from os import EX_TEMPFAIL
import pytest
import requests
from assertpy import assert_that
from api_tests.config_files import config


@pytest.mark.asyncio
class TestCasesSuite:
    """ A test suite for the mock oidc responses """

    @pytest.mark.asyncio
    async def test_cis2_simulated_token_response(self):
        # Given
        expected_status_code = 200
        # This long term id_token expiries on 2023. We will implement a full OIDC provider before that.
        expected_response = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6ImlkZW50aXR5LXNlcnZpY2UtdGVzdHMtMSJ9.eyJhdF9oYXNoIjoidGZfLWxxcHEzNmx3TzdXbVNCSUo2USIsInN1YiI6Ijc4NzgwNzQyOTUxMSIsImF1ZGl0VHJhY2tpbmdJZCI6IjkxZjY5NGU2LTM3NDktNDJmZC05MGIwLWMzMTM0YjBkOThmNi0xNTQ2MzkxIiwiYW1yIjpbIk4zX1NNQVJUQ0FSRCJdLCJpc3MiOiJodHRwczovL2FtLm5oc2ludC5hdXRoLXB0bC5jaXMyLnNwaW5lc2VydmljZXMubmhzLnVrOjQ0My9vcGVuYW0vb2F1dGgyL3JlYWxtcy9yb290L3JlYWxtcy9OSFNJZGVudGl0eS9yZWFsbXMvSGVhbHRoY2FyZSIsInRva2VuTmFtZSI6ImlkX3Rva2VuIiwiYXVkIjoic29tZS1jbGllbnQtaWQiLCJjX2hhc2giOiJiYzd6ekdrQ2xDM01FaUZRM1loUEtnIiwiYWNyIjoiQUFMM19BTlkiLCJvcmcuZm9yZ2Vyb2NrLm9wZW5pZGNvbm5lY3Qub3BzIjoiLUk0NU5qbU1EZE1hLWFORjJzcjloQzdxRUdRIiwic19oYXNoIjoiTFBKTnVsLXdvdzRtNkRzcXhibmluZyIsImF6cCI6InNvbWUtY2xpZW50LWlkIiwiYXV0aF90aW1lIjoxNjEwNTU5ODAyLCJyZWFsbSI6Ii9OSFNJZGVudGl0eS9IZWFsdGhjYXJlIiwiZXhwIjoxNzgxODY1Nzg1LCJ0b2tlblR5cGUiOiJKV1RUb2tlbiIsImlhdCI6MTYyMTg2NTc3NSwic2VsZWN0ZWRfcm9sZWlkIjoiNTU1MjU0MjQyMTAyIn0.ny8CczDjFqaa1rsq0O2YQ94gr-Cm4VP2_T5V29VIRphRIjCnEwcd6KU1PQR6eUW86kEGLV28isHkED4_4ByFLhJQFK3MJ-rvqSgK7PArqxPUT5Qq5SJ-9u9m03b5BV6jws4ofA4IYp3JH_N34SbePAGPtW5AHSRuwMjnz25ctUrikahSfPw9I7MRmBs9EUZpTqzUzXpl5-yqna1PVTaVzNcYHHP7n4sfJblACTX6vUqz_XAKA72mvBmY_UYCyuB99PpNZIv1p2ytH3FNm40DwJGFNng5B1c_bCT-jGCcOdERpp_DGtica91K8Ex1F04cjs6llpx9YE9uvz-6fMdQng"

        # When
        response = requests.post(
            url=config.MOCK_PROXY_BASE_PATH + "/cis2_simulated_token"
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_response).is_equal_to(response.json()["id_token"])

    @pytest.mark.asyncio
    async def test_cis2_public_key_response(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.MOCK_PROXY_BASE_PATH + "/identity-service/jwks"
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.asyncio
    async def test_nhs_login_public_key_response(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(
            url=config.MOCK_PROXY_BASE_PATH + "/identity-service/nhs-login-jwks"
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.asyncio
    async def test_nhs_login_simulated_token_response(self):
        # Given
        expected_status_code = 200
        # This long term id_token expiries on 2023. We will implement a full OIDC provider before that.
        expected_response = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzUxMiIsImtpZCI6Im5ocy1sb2dpbiIsInN1YiI6IjQ5ZjQ3MGExLWNjNTItNDliNy1iZWJhLTBmOWNlYzkzN2M0NiIsImF1ZCI6InNvbWUtY2xpZW50LWlkIiwiaXNzIjoiaHR0cHM6Ly9pbnRlcm5hbC1kZXYuYXBpLnNlcnZpY2UubmhzLnVrIiwiZXhwIjoxNjgzMzMxMTY2LCJpYXQiOjE2MjM4NDkyNzEsImp0aSI6IjhlZGFiZTJiLWM3ZmYtNDBiZC1iYzdmLTBiOGRjNmE1MjQyMyJ9.eyJzdWIiOiI0OWY0NzBhMS1jYzUyLTQ5YjctYmViYS0wZjljZWM5MzdjNDYiLCJiaXJ0aGRhdGUiOiIxOTY4LTAyLTEyIiwibmhzX251bWJlciI6Ijk5MTIwMDMwNzEiLCJpc3MiOiJodHRwczovL2ludGVybmFsLWRldi5hcGkuc2VydmljZS5uaHMudWsiLCJ2dG0iOiJodHRwczovL2F1dGguc2FuZHBpdC5zaWduaW4ubmhzLnVrL3RydXN0bWFyay9hdXRoLnNhbmRwaXQuc2lnbmluLm5ocy51ayIsImF1ZCI6InNvbWUtY2xpZW50LWlkIiwiaWRfc3RhdHVzIjoidmVyaWZpZWQiLCJ0b2tlbl91c2UiOiJpZCIsInN1cm5hbWUiOiJNSUxMQVIiLCJhdXRoX3RpbWUiOjE2MjM4NDkyMDEsInZvdCI6IlA5LkNwLkNkIiwiaWRlbnRpdHlfcHJvb2ZpbmdfbGV2ZWwiOiJQOSIsImV4cCI6MTc4MzMzMTE2NiwiaWF0IjoxNjIzODQ5MjcxLCJmYW1pbHlfbmFtZSI6Ik1JTExBUiIsImp0aSI6IjhlZGFiZTJiLWM3ZmYtNDBiZC1iYzdmLTBiOGRjNmE1MjQyMyJ9.JFjQHnnvHjwFrI-i_qpZ70Ws59e4GtxjR55Sz2qa_XecqbtHlam_JwRZOqcU5Rt1lgIpWsW4e0n7hB7yvMt-TR65C23GMzXnX0fklbvZ-b7uz4NjpYQKPr6bwOJioOYglXk_kR4wnZZzH6L5cZMcgv6morTEQnHvaqXmtRV5WEUKmNP-ISlHBGuFgaVJvVc95so2MGIanfrsUW2ZcnRwYQggZrRrAPwsJ2gfRxuoIMImmpFT5e7QG3j2TjcJjXdn6SpwlRa1ji9Y2qjyE284VHG2HKTQZLDmBImJD9UTJwUY2TiaCMV6gHOAp2tJQW94LwXmtgCrX9HQloXw3RfMx_HeBGjXJYBTXTzNrySMxSPVOu4pIJIq7VDlO8Za5q9TuWE820TfBWUdyaKAZtMILb7VMS7ftxnhMySs93hqhiEJc_7zOkaOAAEHlhan0xyS7aCaj00GArfNQUucLSaH3lmF7SlRY6lKHndIrwV7nvtc-0TT1wh_HY9mFdrBL5tryD-vTi_CaOD0Gzesx3bb4eFZI3CuCDfXZzM7TY_YuGUPe3G3Bp_OdGdNpzUPyToJTu3tgdEJM5GCRDtWCBupjrBY7ECWqlpc1bF2VUqL5YWmxU5JGnA0_1oU6RdCbiz1fGcRPNAtPrbSUywZNvQPGkHExufqeXm293Ltmqq73A4"

        # When
        response = requests.post(
            url=config.MOCK_PROXY_BASE_PATH + "/nhs_login_simulated_token",
            data={"client_assertion": "1234"},
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_response).is_equal_to(response.json()["id_token"])

    @pytest.mark.asyncio
    async def test_userinfo_response(self):
        # Given
        expected_status_code = 200

        # When
        response = requests.get(url=config.MOCK_PROXY_BASE_PATH + "/userinfo")

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(response.json()).is_not_equal_to({})

    @pytest.mark.asyncio
    async def test_client_credentials(self, get_token_client_credentials):
        # Given
        expected_body_keys = ["access_token", "expires_in", "token_type", "issued_at"]

        # When
        token_response = get_token_client_credentials

        # Then
        assert_that(list(token_response.keys())).is_equal_to(expected_body_keys)

    @pytest.mark.asyncio
    async def test_cis2_token_exchange(self, get_token_cis2_token_exchange):
        # Given
        expected_body_keys = [
            "access_token",
            "expires_in",
            "token_type",
            "issued_token_type",
            "refresh_token",
            "refresh_token_expires_in",
            "refresh_count",
        ]

        # When
        token_response = get_token_cis2_token_exchange

        # Then
        assert_that(list(token_response.keys())).is_equal_to(expected_body_keys)

    @pytest.mark.asyncio
    async def test_nhs_login_token_exchange(self, get_token_nhs_login_token_exchange):
        # Given
        expected_body_keys = [
            "access_token",
            "expires_in",
            "token_type",
            "issued_token_type",
            "refresh_token",
            "refresh_token_expires_in",
            "refresh_count",
        ]

        # When
        token_response = get_token_nhs_login_token_exchange

        # Then
        assert_that(list(token_response.keys())).is_equal_to(expected_body_keys)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("auth_method", ["P0", "P5", "P9"])
    async def test_auth_code_nhs_login(self, get_token_auth_code_nhs_login):
        # Given
        expected_body_keys = [
            "access_token",
            "expires_in",
            "refresh_token",
            "refresh_token_expires_in",
            "refresh_count",
            "token_type",
            "sid"
        ]

        # When
        token_response = get_token_auth_code_nhs_login

        # Then
        assert_that(list(token_response.keys())).is_equal_to(expected_body_keys)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("auth_method", ["N3_SMARTCARD", "FIDO2", "IOS"])
    async def test_auth_code_nhs_cis2(self, get_token_auth_code_nhs_cis2):
        # Given
        expected_body_keys = [
            "access_token",
            "expires_in",
            "refresh_token",
            "refresh_token_expires_in",
            "refresh_count",
            "token_type",
            "sid"
        ]

        # When
        token_response = get_token_auth_code_nhs_cis2

        # Then
        assert_that(list(token_response.keys())).is_equal_to(expected_body_keys)
