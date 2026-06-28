CREATE TABLE IF NOT EXISTS carts (
    id CHAR(36) PRIMARY KEY,
    status ENUM('active', 'finalized') NOT NULL DEFAULT 'active',
    total_value DECIMAL(12, 2) NOT NULL DEFAULT 0,
    supermarket VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finalized_at TIMESTAMP NULL,
    INDEX idx_carts_status (status)
);

CREATE TABLE IF NOT EXISTS products (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255) NULL,
    category VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cart_items (
    id CHAR(36) PRIMARY KEY,
    cart_id CHAR(36) NOT NULL,
    product_id CHAR(36) NOT NULL,
    total_price DECIMAL(12, 2) NOT NULL,
    quantity DECIMAL(12, 4) NOT NULL,
    unit VARCHAR(10) NOT NULL,
    purchased_quantity DECIMAL(12, 4) NOT NULL DEFAULT 1,
    price_type ENUM('normal', 'wholesale') NOT NULL DEFAULT 'normal',
    wholesale_min_quantity DECIMAL(12, 4) NULL,
    unit_price DECIMAL(12, 4) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cart_items_cart FOREIGN KEY (cart_id) REFERENCES carts (id),
    CONSTRAINT fk_cart_items_product FOREIGN KEY (product_id) REFERENCES products (id),
    INDEX idx_cart_items_cart_id (cart_id)
);
