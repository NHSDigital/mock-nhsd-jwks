from api_tests.config_files.environments import ENV

# Mock Proxy
MOCK_PROXY_BASE_URL = ENV["mock_proxy"]["base_url"]
MOCK_PROXY_PATH = ENV["mock_proxy"]["proxy_path"]
MOCK_PROXY_NAME = ENV["mock_proxy"]["proxy_name"]
MOCK_PROXY_BASE_PATH = f"{MOCK_PROXY_BASE_URL}/{MOCK_PROXY_PATH}/"

# JWT variables
JWT_PRIVATE_KEY_ABSOLUTE_PATH = ENV["jwt_private_key_absolute_path"]
ID_TOKEN_NHS_LOGIN_PRIVATE_KEY_ABSOLUTE_PATH = ENV["id_token_nhs_login_private_key_absolute_path"]
ID_TOKEN_PRIVATE_KEY_ABSOLUTE_PATH = ENV["id_token_private_key_absolute_path"]