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
    }
}
