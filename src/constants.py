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

display_menu = """----- MENU -----\n
1. Quel aliment souhaitez-vous remplacer ?
2. Retrouver mes aliments substitués.
\nq. Quitter.
\n-- Entrer votre réponse: """

display_categories = """\n----- CATEGORIES -----\n
{}. {}\n{}. {}\n{}. {}\n{}. {}\n{}. {}\n\nb. Retour\nq. Quitter
\n-- Entrer votre réponse: """

display_products = """{}. {name}"""

display_chosen_product = """
Marque: {brand}
Point de vente: {store}
Nutriscore: {nutriscore}
{url}\n"""

display_substitutes = """{}. {name}\nNutriscore: {nutriscore}\n"""

category = """SELECT * from category ORDER BY id"""

product = """
    SELECT code, product.name
    FROM product
    WHERE category_id = :cat_id
    AND nutriscore BETWEEN 'C' AND 'E'
    ORDER BY RAND()
    LIMIT 10"""

chosen_product = """
    SELECT
    product.code, product.name as product,
    brand, store.name as store, nutriscore, url
    FROM product
    LEFT JOIN store_product
    ON product.code = product_code
    LEFT JOIN store
    ON store.id = store_id
    WHERE product.code = :identification"""

substitute = """
    SELECT code, name, nutriscore
    FROM product
    WHERE category_id = :cat_id
    AND nutriscore BETWEEN 'A' AND 'B'
    ORDER BY RAND()
    LIMIT 5"""
