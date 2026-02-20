-- Включение поддержки внешних ключей (обязательно)
PRAGMA foreign_keys = ON;

-- Таблица категорий товаров
CREATE TABLE IF NOT EXISTS main_category (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  VARCHAR(100) NOT NULL UNIQUE
);

-- Таблица производителей
CREATE TABLE IF NOT EXISTS main_manufacturer (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  VARCHAR(100) NOT NULL UNIQUE
);

-- Таблица поставщиков
CREATE TABLE IF NOT EXISTS main_supplier (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  VARCHAR(100) NOT NULL UNIQUE
);

-- Таблица товаров
CREATE TABLE IF NOT EXISTS main_product (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    article           VARCHAR(20) NOT NULL UNIQUE,
    name              VARCHAR(200) NOT NULL,
    unit              VARCHAR(20) NOT NULL,
    price             NUMERIC NOT NULL,
    discount          INTEGER NOT NULL DEFAULT 0,
    quantity_in_stock INTEGER NOT NULL DEFAULT 0,
    description       TEXT NOT NULL,
    photo             VARCHAR(100),
    category_id       INTEGER NOT NULL,
    manufacturer_id   INTEGER NOT NULL,
    supplier_id       INTEGER NOT NULL,
    FOREIGN KEY (category_id)     REFERENCES main_category(id)     ON DELETE RESTRICT,
    FOREIGN KEY (manufacturer_id) REFERENCES main_manufacturer(id) ON DELETE RESTRICT,
    FOREIGN KEY (supplier_id)     REFERENCES main_supplier(id)     ON DELETE RESTRICT
);

-- Таблица профилей пользователей (расширение модели User Django)
CREATE TABLE IF NOT EXISTS main_profile (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(150) NOT NULL,
    role      VARCHAR(20) NOT NULL,
    user_id   INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE
);

-- Таблица пунктов выдачи
CREATE TABLE IF NOT EXISTS main_pickuppoint (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    address VARCHAR(300) NOT NULL UNIQUE
);

-- Таблица заказов
CREATE TABLE IF NOT EXISTS main_order (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number    INTEGER NOT NULL UNIQUE,
    order_date      DATE NOT NULL,
    delivery_date   DATE NOT NULL,
    pickup_code     VARCHAR(20) NOT NULL,
    status          VARCHAR(20) NOT NULL,
    client_id       INTEGER NOT NULL,
    pickup_point_id INTEGER NOT NULL,
    FOREIGN KEY (client_id)       REFERENCES main_profile(id)     ON DELETE RESTRICT,
    FOREIGN KEY (pickup_point_id) REFERENCES main_pickuppoint(id) ON DELETE RESTRICT
);

-- Таблица позиций заказа
CREATE TABLE IF NOT EXISTS main_orderitem (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    quantity   INTEGER NOT NULL,
    order_id   INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (order_id)   REFERENCES main_order(id)   ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES main_product(id) ON DELETE RESTRICT
);

-- Индексы для ускорения запросов
CREATE INDEX IF NOT EXISTS idx_product_category     ON main_product(category_id);
CREATE INDEX IF NOT EXISTS idx_product_manufacturer ON main_product(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_product_supplier     ON main_product(supplier_id);
CREATE INDEX IF NOT EXISTS idx_profile_user         ON main_profile(user_id);
CREATE INDEX IF NOT EXISTS idx_order_client         ON main_order(client_id);
CREATE INDEX IF NOT EXISTS idx_order_pickup         ON main_order(pickup_point_id);
CREATE INDEX IF NOT EXISTS idx_orderitem_order      ON main_orderitem(order_id);
CREATE INDEX IF NOT EXISTS idx_orderitem_product    ON main_orderitem(product_id);