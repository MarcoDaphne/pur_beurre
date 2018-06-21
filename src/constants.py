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

list_name = """SELECT name FROM client"""

check_password = """
    SELECT
        password
    FROM
        client
    WHERE
        name = :name"""

id_client = """
    SELECT
        id
    FROM
        client
    WHERE
        name = :name"""

register_client = """
    INSERT INTO
        client (name, password)
    VALUES
        (:name, :password)
    ON DUPLICATE KEY UPDATE name = :name"""

r_substitute = """
    INSERT INTO
        favorite (client_id, product_id)
    VALUES
        (:c_id, :p_id)"""

display_menu = """----- MENU -----\n
1. Quel aliment souhaitez-vous remplacer ?
2. Retrouver mes aliments substitués.
\nq. Quitter.
\n-- Entrer votre réponse: """

display_categories = """\nb. Retour
q. Quitter
\n- Sélectionnez une catégorie: """

display_products = """\nb. Retour
q. Quitter
\nSélectionnez un produit: """

display_chosen_substitute = """\nr. Enregistrer
b. Retour
q. Quitter
\nEntrer votre réponse: """

chosen_substitute = """Marque: {brand}
Point de vente: {store}
Nutriscore: {nutriscore}
{url}\n"""

display_substitutes = """\nb. Retour
q. Quitter
\nSélectionnez un substitut: """

display_login_menu = """\n----- INSCRIPTION - CONNEXION -----\n
1. Se connecter
2. S'inscrire
b. Retour
q. Quitter
\nSélectionnez une réponse: """

display_favorite = """
    SELECT 
    product.name as substitut, brand, store.name as store, nutriscore, url
    FROM product
    INNER JOIN favorite
    ON product_id = product.code
    INNER JOIN client
    ON client.id = favorite.client_id
    LEFT JOIN store_product
    ON product.code = product_code
    LEFT JOIN store
    ON store.id = store_id
    where client.id = :client"""


category = """SELECT * from category ORDER BY id"""

product = """
    SELECT name
    FROM product
    WHERE category_id = :cat_id
    AND nutriscore BETWEEN 'C' AND 'E'
    ORDER BY RAND()
    LIMIT 10"""

chosen_product = """
    SELECT
    product.code, product.name as substitute,
    brand, store.name as store, nutriscore, url
    FROM product
    LEFT JOIN store_product
    ON product.code = product_code
    LEFT JOIN store
    ON store.id = store_id
    WHERE product.code = :code"""

substitute = """
    SELECT code, name, nutriscore
    FROM product
    WHERE category_id = :cat_id
    AND nutriscore BETWEEN 'A' AND 'B'
    ORDER BY RAND()
    LIMIT 5"""
