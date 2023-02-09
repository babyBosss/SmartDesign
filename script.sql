CREATE TABLE IF NOT EXISTS product(
                                      vendor_code TEXT PRIMARY KEY,
                                      name TEXT NOT NULL,
                                      brand TEXT NOT NULL,
                                      selling_price numeric NOT NULL
);

CREATE TABLE IF NOT EXISTS cart(
                                   vendor_code  TEXT REFERENCES product(vendor_code) on update cascade UNIQUE,
                                   amount INT NOT NULL,
                                   total_price numeric NOT NULL
);



INSERT INTO product (vendor_code, name, brand, selling_price) VALUES ('10CMA456XXH', 'iPhone 14', 'Apple', 99000);
INSERT INTO product (vendor_code, name, brand, selling_price) VALUES ('XDLWNGIPQWMKR', 'Galaxy S8', 'Samsung', 54990);
INSERT INTO product (vendor_code, name, brand, selling_price) VALUES ('XIAMM17748493', 'POCO X5 Pro', 'Xiaomi', 12490);
INSERT INTO product (vendor_code, name, brand, selling_price) VALUES ('120874054', 'Nova Y70', 'Huawei', 10990);
