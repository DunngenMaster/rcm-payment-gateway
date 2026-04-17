CREATE_MERCHANTS_TABLE = """
CREATE TABLE IF NOT EXISTS merchants (
    merchant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clover_merchant_id VARCHAR(255) UNIQUE NOT NULL,
    clover_access_token BYTEA NOT NULL,
    merchant_name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_merchants_clover_merchant_id ON merchants(clover_merchant_id);
"""

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    merchant_id UUID UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_merchant_id ON users(merchant_id);
"""

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL,
    clover_order_id VARCHAR(255),
    title VARCHAR(255) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    total FLOAT NOT NULL DEFAULT 0.0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE
);

CREATE INDEX idx_orders_merchant_id ON orders(merchant_id);
CREATE INDEX idx_orders_clover_order_id ON orders(clover_order_id);
"""

CREATE_LINE_ITEMS_TABLE = """
CREATE TABLE IF NOT EXISTS line_items (
    line_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL,
    merchant_id UUID NOT NULL,
    clover_line_item_id VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE
);

CREATE INDEX idx_line_items_order_id ON line_items(order_id);
CREATE INDEX idx_line_items_merchant_id ON line_items(merchant_id);
"""

CREATE_PAYMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS payments (
    payment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID NOT NULL,
    order_id UUID NOT NULL,
    clover_payment_id VARCHAR(255),
    amount FLOAT NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    token VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

CREATE INDEX idx_payments_merchant_id ON payments(merchant_id);
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_clover_payment_id ON payments(clover_payment_id);
"""

GET_MERCHANT = "SELECT * FROM merchants WHERE merchant_id = %s;"

GET_USER_BY_EMAIL = "SELECT * FROM users WHERE email = %s;"

GET_MERCHANT_ORDERS = "SELECT * FROM orders WHERE merchant_id = %s ORDER BY created_at DESC;"

GET_ORDER_LINE_ITEMS = "SELECT * FROM line_items WHERE order_id = %s AND merchant_id = %s;"

GET_ORDER_PAYMENTS = "SELECT * FROM payments WHERE order_id = %s AND merchant_id = %s;"

GET_PAYMENT_STATS = """
SELECT 
    status,
    COUNT(*) as count,
    SUM(amount) as total_amount
FROM payments
WHERE merchant_id = %s
GROUP BY status;
"""

INSERT_MERCHANT = """
INSERT INTO merchants (clover_merchant_id, clover_access_token, merchant_name)
VALUES (%s, %s, %s)
RETURNING merchant_id;
"""

INSERT_USER = """
INSERT INTO users (email, password_hash, merchant_id)
VALUES (%s, %s, %s)
RETURNING user_id;
"""

INSERT_ORDER = """
INSERT INTO orders (merchant_id, clover_order_id, title, currency)
VALUES (%s, %s, %s, %s)
RETURNING order_id;
"""

INSERT_LINE_ITEM = """
INSERT INTO line_items (order_id, merchant_id, clover_line_item_id, name, price, quantity)
VALUES (%s, %s, %s, %s, %s, %s)
RETURNING line_item_id;
"""

INSERT_PAYMENT = """
INSERT INTO payments (merchant_id, order_id, clover_payment_id, amount, currency, status, token)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING payment_id;
"""

UPDATE_PAYMENT_STATUS = """
UPDATE payments 
SET status = %s, updated_at = CURRENT_TIMESTAMP
WHERE payment_id = %s AND merchant_id = %s
RETURNING *;
"""
