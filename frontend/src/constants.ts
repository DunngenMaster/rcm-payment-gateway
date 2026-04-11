// Frontend Constants

// API Configuration
export const API_BASE_URL = "http://localhost:8000";

// API Endpoints
export const AUTH_START = "/auth/start";
export const AUTH_EXCHANGE = "/auth/exchange";
export const PAYMENT_ORDER = "/payment/order";
export const PAYMENT_LINE_ITEM = "/payment/line-item";
export const PAYMENT_ECOMMERCE_KEY = "/payment/ecommerce-key";
export const PAYMENT_TOKENIZE_CARD = "/payment/tokenize-card";
export const PAYMENT_CHARGE = "/payment/charge";

// HTTP Methods
export const METHOD_GET = "GET";
export const METHOD_POST = "POST";

// Headers
export const HEADER_CONTENT_TYPE = "Content-Type";
export const CONTENT_TYPE_JSON = "application/json";

// Default Values
export const DEFAULT_CARD_NUMBER = "4242424242424242";
export const DEFAULT_EXP_MONTH = "12";
export const DEFAULT_EXP_YEAR = "2030";
export const DEFAULT_CVV = "123";
export const DEFAULT_ZIP = "12345";
export const DEFAULT_QUANTITY = "1";
export const DEFAULT_CURRENCY = "usd";

// Messages
export const MSG_WELCOME = "Welcome to Clover Payment Gateway";
export const MSG_CONNECTING = "Exchanging Clover authorization code...";
export const MSG_CONNECTED = "Clover connected successfully!";
export const MSG_CONNECT_FAILED = "Failed to connect Clover.";
export const MSG_CONNECT_ERROR = "Error while connecting Clover.";

export const MSG_ORDER_CREATE = "Order created: ";
export const MSG_ORDER_FAILED = "Failed to create order";
export const MSG_ITEM_ADDED = "Item added to order";
export const MSG_ITEM_FAILED = "Failed to add item";

export const MSG_ECOMMERCE_KEY_FETCH = "Fetching Ecommerce key...";
export const MSG_ECOMMERCE_KEY_READY = "Ecommerce key ready";
export const MSG_ECOMMERCE_KEY_FAILED = "Failed to get Ecommerce key";
export const MSG_ECOMMERCE_KEY_REQUIRED = "Get Ecommerce key first";

export const MSG_CARD_TOKENIZING = "Tokenizing card...";
export const MSG_CARD_TOKENIZED = "Card tokenized: ";
export const MSG_CARD_TOKENIZE_FAILED = "Tokenization failed: ";
export const MSG_CARD_TOKENIZE_ERROR = "Tokenization error: ";

export const MSG_PAYMENT_PROCESSING = "Processing payment...";
export const MSG_PAYMENT_SUCCESSFUL = "Payment successful! ID: ";
export const MSG_PAYMENT_FAILED = "Payment failed: ";
export const MSG_PAYMENT_ERROR = "Payment error: ";

// Local Storage Keys
export const STORAGE_MERCHANT_ID = "clover_merchant_id";

// URL Parameters
export const PARAM_CODE = "code";
export const PARAM_MERCHANT_ID = "merchant_id";
export const PARAM_AUTH = "auth";
export const PARAM_SUCCESS = "success";
