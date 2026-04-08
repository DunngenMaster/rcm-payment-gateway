"""
Centralized constants for the RCM Workflow API.
Contains all hardcoded strings organized by category.
"""

# ============================================================================
# API Configuration
# ============================================================================
API_TITLE = "RCM Workflow API"
API_VERSION = "1.0"

# ============================================================================
# CORS Configuration
# ============================================================================
CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# ============================================================================
# Routes and Router Tags
# ============================================================================
HEALTH_ROUTER_TAG = "health"
HEALTH_ROUTE_PATH = "/health"

AUTH_ROUTER_PREFIX = "/auth"
AUTH_ROUTER_TAG = "auth"
AUTH_START_ROUTE = "/start"
AUTH_CALLBACK_ROUTE = "/callback"

# ============================================================================
# Response Keys and Values
# ============================================================================
HEALTH_STATUS_KEY = "status"
HEALTH_STATUS_OK = "ok"

AUTH_SUCCESS_QUERY_PARAM = "?auth=success"

# ============================================================================
# OAuth Configuration
# ============================================================================
OAUTH_PARAM_CLIENT_ID = "client_id"
OAUTH_PARAM_RESPONSE_TYPE = "response_type"
OAUTH_RESPONSE_TYPE_CODE = "code"
OAUTH_PARAM_REDIRECT_URI = "redirect_uri"

OAUTH_PAYLOAD_CLIENT_ID = "client_id"
OAUTH_PAYLOAD_CLIENT_SECRET = "client_secret"
OAUTH_PAYLOAD_CODE = "code"
OAUTH_PAYLOAD_REDIRECT_URI = "redirect_uri"

OAUTH_AUTHORIZE_ENDPOINT = "/oauth/v2/authorize"
OAUTH_TOKEN_ENDPOINT = "/oauth/v2/token"
# ============================================================================
# HTTP Headers and Content Types
# ============================================================================
HEADER_AUTHORIZATION = "Authorization"
HEADER_CONTENT_TYPE = "Content-Type"

AUTH_SCHEME_BEARER = "Bearer "

CONTENT_TYPE_JSON = "application/json"

# ============================================================================
# Database/Storage
# ============================================================================
TOKEN_FILE_PATH = "app/db/token.json"
TOKEN_JSON_KEY_ACCESS_TOKEN = "access_token"

FILE_MODE_READ = "r"
FILE_MODE_WRITE = "w"

# ============================================================================
# Error Messages
# ============================================================================
ERROR_NO_ACCESS_TOKEN = "Access token not found. Please authenticate with Clover first."


