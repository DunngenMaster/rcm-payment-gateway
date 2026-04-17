API_TITLE = "RCM Workflow API"
API_VERSION = "1.0"

# CORS Configuration
CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Routes and Router Tags
HEALTH_ROUTER_TAG = "health"
HEALTH_ROUTE_PATH = "/health"

AUTH_ROUTER_PREFIX = "/auth"
AUTH_ROUTER_TAG = "auth"
AUTH_START_ROUTE = "/start"
AUTH_EXCHANGE_ROUTE = "/exchange"

PAYMENT_ROUTER_PREFIX = "/payment"
PAYMENT_ROUTER_TAG = "payment"
PAYMENT_ROUTE_ORDER = "/order"
PAYMENT_ROUTE_LINE_ITEM = "/line-item"
PAYMENT_ROUTE_ECOMMERCE_KEY = "/ecommerce-key"
PAYMENT_ROUTE_TOKENIZE = "/tokenize-card"
PAYMENT_ROUTE_CHARGE = "/charge"
PAYMENT_ROUTE_TRANSACTIONS = "/transactions"

# Response Keys and Values
HEALTH_STATUS_KEY = "status"
HEALTH_STATUS_OK = "ok"

# OAuth Configuration
OAUTH_PARAM_CLIENT_ID = "client_id"
OAUTH_PARAM_RESPONSE_TYPE = "response_type"
OAUTH_RESPONSE_TYPE_CODE = "code"
OAUTH_PARAM_REDIRECT_URI = "redirect_uri"
OAUTH_PARAM_MERCHANT_ID = "merchant_id"

OAUTH_PAYLOAD_CLIENT_ID = "client_id"
OAUTH_PAYLOAD_CLIENT_SECRET = "client_secret"
OAUTH_PAYLOAD_CODE = "code"
OAUTH_PAYLOAD_REDIRECT_URI = "redirect_uri"

OAUTH_AUTHORIZE_ENDPOINT = "/oauth/v2/authorize"
OAUTH_TOKEN_ENDPOINT = "/oauth/v2/token"

# HTTP Headers and Content Types
HEADER_AUTHORIZATION = "Authorization"
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_ACCEPT = "Accept"
HEADER_X_FORWARDED_FOR = "x-forwarded-for"
HEADER_API_KEY = "apikey"

AUTH_SCHEME_BEARER = "Bearer "

CONTENT_TYPE_JSON = "application/json"

# Clover API Endpoints
CLOVER_PAKMS_ENDPOINT = "/pakms/apikey"
CLOVER_CHARGES_ENDPOINT = "/v1/charges"
CLOVER_TOKENS_ENDPOINT = "/v1/tokens"
CLOVER_TOKEN_SANDBOX_URL = "https://token-sandbox.dev.clover.com"

# Clover Payment Parameters
CLOVER_ECOMIND_ECOM = "ecom"
CLOVER_CARD_KEY = "card"
CLOVER_CARD_NUMBER = "number"
CLOVER_CARD_EXP_MONTH = "exp_month"
CLOVER_CARD_EXP_YEAR = "exp_year"
CLOVER_CARD_CVV = "cvv"
CLOVER_CARD_ZIP = "zip"

# Transaction Status
TRANSACTION_STATUS_SUCCESS = "success"
TRANSACTION_TYPE_CHARGE = "charge"

# Database/Storage
TOKEN_FILE_PATH = "app/db/token.json"
TOKEN_JSON_KEY_ACCESS_TOKEN = "access_token"

FILE_MODE_READ = "r"
FILE_MODE_WRITE = "w"

# Error Messages
ERROR_NO_ACCESS_TOKEN = "No access token. Authenticate with Clover first."
ERROR_AMOUNT_SOURCE_REQUIRED = "Amount and source are required"

# HTTP Status Codes
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500

# Default Values
DEFAULT_ORDER_TITLE = "Demo Order"
DEFAULT_ORDER_CURRENCY = "USD"
DEFAULT_CHARGE_CURRENCY = "usd"
DEFAULT_CHARGE_DESCRIPTION = "Demo Clover charge"
DEFAULT_LINE_ITEM_QUANTITY = 1

# Request Field Names and Response Keys
RESPONSE_KEY_SUCCESS = "success"
RESPONSE_KEY_MESSAGE = "message"
RESPONSE_KEY_ORDER = "order"
RESPONSE_KEY_LINE_ITEM = "line_item"
RESPONSE_KEY_KEY_DATA = "key_data"
RESPONSE_KEY_TOKEN_DATA = "token_data"
RESPONSE_KEY_PAYMENT = "payment"
RESPONSE_KEY_TRANSACTIONS = "transactions"

# Transaction Type and Log Keys
TRANSACTION_LOG_TYPE_ORDER_CREATED = "order_created"
TRANSACTION_LOG_TYPE_LINE_ITEM_ADDED = "line_item_added"
TRANSACTION_LOG_KEY_ORDER_ID = "order_id"
TRANSACTION_LOG_KEY_TITLE = "title"
TRANSACTION_LOG_KEY_NAME = "name"
TRANSACTION_LOG_KEY_PRICE = "price"

# Response Messages
MSG_ORDER_CREATED = "Order created"
MSG_ITEM_ADDED = "Item added"
MSG_ECOMMERCE_KEY_FETCHED = "Ecommerce key fetched successfully"
MSG_CARD_TOKENIZED = "Card tokenized successfully"
MSG_CHARGE_CREATED = "Charge created successfully"
MSG_AUTH_CONNECTED = "Clover connected successfully"


