from api_tests.config_files.environments import ENV

# Api details
APIGEE_CLIENT_ID = ENV['oauth']['apigee_client_id']
BASE_URL = ENV['oauth']['base_url']
AUTHORIZE_URL = f"{BASE_URL}/authorize"
TOKEN_URL = f"{BASE_URL}/token"

# Apigee API details
APIGEE_API_URL = ENV['apigee']['base_url']
APIGEE_AUTHENTICATION = ENV['apigee']['api_authentication']
APIGEE_ENVIRONMENT = "internal-dev"
APIGEE_USERNAME = ENV['apigee']['username']
APIGEE_PASSWORD = ENV['apigee']['password']
APIGEE_ORGANISATION = ENV['apigee']['organisation']

# Reasonable Adjustments
MOCK_PROXY_BASE_URL = ENV['mock_proxy']['base_url']
MOCK_PROXY_PATH = ENV['mock_proxy']['proxy_path']
MOCK_PROXY_NAME = ENV['mock_proxy']['proxy_name']
USER_ROLE_SHARED_FLOW = f"{MOCK_PROXY_BASE_URL}/{MOCK_PROXY_PATH}/user-info-service"

# Authentication provider (Simulated OAuth)
AUTHENTICATE_URL = ENV['oauth']['authenticate_url']

# Endpoints
ENDPOINTS = {
    'authorize': AUTHORIZE_URL,
    'token': TOKEN_URL,
    'authenticate': AUTHENTICATE_URL,
}

# App details
INTERNAL_TESTING_INTERNAL_DEV = {
    'client_id': ENV['oauth']['client_id'],
    'client_secret': ENV['oauth']['client_secret'],
    'redirect_url': ENV['apps']['internal_testing_internal_dev']['redirect_url'],
    'endpoints': ENDPOINTS
}
