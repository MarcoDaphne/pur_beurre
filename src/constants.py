url = 'https://fr.openfoodfacts.org/cgi/search.pl'
connexion = "mysql+pymysql://testeur:camomille@localhost/test?charset=utf8mb4"
directory = "sql"
create_table = 'create_table.sql'
categories = [
    'pizza',
    'steack hache',
    'pates a tartiner',
    'creme glacee',
    'soda']
ngrad_a = 'A'
ngrad_b = 'B'
ngrad_c = 'C'
ngrad_d = 'D'
ngrad_e = 'E'
comma = ','
rds_prod = """
    INSERT INTO
        product (code, name, brand, url, nutriscore, category_id)
    VALUES
        (:code, :name, :brand, :url, :nutriscore,
        (SELECT id FROM category WHERE name = :cat_name))"""

rds_cat = """
    INSERT INTO
        category (name)
    VALUES
        (:name)"""

rds_store = """
    INSERT INTO
        store (name)
    VALUES
        (:name)
    ON DUPLICATE KEY UPDATE name = :name"""

rds_str_prod = """
    INSERT INTO
        store_product (store_id, product_code)
    VALUES
        ((SELECT id FROM store WHERE name = :store), :code)"""

sel_cat = """SELECT * from category"""

category_id = """SELECT id FROM category"""

sel_prod = """
    SELECT code, product.name, store.name as store, brand, nutriscore, url
    FROM product
    INNER JOIN store_product
    ON product.code = product_code
    INNER JOIN store
    ON store.id = store_id
    WHERE category_id = :cat_id
    AND nutriscore BETWEEN 'A' AND 'B'
    GROUP BY product.name
    LIMIT 5
    UNION
    SELECT code, product.name, store.name as store, brand, nutriscore, url
    FROM product
    INNER JOIN store_product
    ON product.code = product_code
    INNER JOIN store
    ON store.id = store_id
    WHERE category_id = :cat_id
    AND nutriscore BETWEEN 'C' AND 'E'
    GROUP BY product.name
    LIMIT 15"""

product = """
    SELECT code, product.name, store.name as store, brand, nutriscore, url
    FROM product
    INNER JOIN store_product
    ON product.code = product_code
    INNER JOIN store
    ON store.id = store_id
    WHERE product.code = :cod"""
