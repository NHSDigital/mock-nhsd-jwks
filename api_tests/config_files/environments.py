import os
from dotenv import load_dotenv

load_dotenv()

# Configure Test Environment
def get_env(variable_name: str, default: str = "") -> str:
    """Returns a environment variable"""
    try:
        return os.environ[variable_name]
    except KeyError:
        return default


ENV = {
    "mock_proxy": {
        "base_url": os.getenv("OAUTH_BASE_URI"),
        "proxy_path": os.getenv("MOCK_PROXY"),
        "proxy_name": os.getenv("MOCK_PROXY_NAME"),
    },
    "jwt_private_key_absolute_path": get_env("JWT_PRIVATE_KEY_ABSOLUTE_PATH"),
    "id_token_nhs_login_private_key_absolute_path": get_env("ID_TOKEN_NHS_LOGIN_PRIVATE_KEY_ABSOLUTE_PATH"),
    "id_token_private_key_absolute_path": get_env("ID_TOKEN_PRIVATE_KEY_ABSOLUTE_PATH"),
}
