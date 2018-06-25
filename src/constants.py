url = 'https://fr.openfoodfacts.org/cgi/search.pl'
connexion = "mysql+pymysql://testeur:camomille@localhost/test?charset=utf8mb4"
directory = "sql"
create_table = 'create_table.sql'
categories = [
    'Charcuterie',
    'Fromage',
    'Légume',
    'Pizza',
    'Chocolat']
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

list_email = """SELECT email FROM client"""

check_password = """
    SELECT
        password
    FROM
        client
    WHERE
        email = :email"""

id_client = """
    SELECT
        id
    FROM
        client
    WHERE
        email = :email"""

register_client = """
    INSERT INTO
        client (email, password)
    VALUES
        (:email, :password)
    ON DUPLICATE KEY UPDATE email = :email"""

record_substitute = """
    INSERT INTO
        favorite (client_id, product_id)
    VALUES
        (:client_id, :product_id)"""

display_menu = """\n------ MENU PRINCIPALE ------\n
1. Quel aliment souhaitez-vous remplacer ?
2. Retrouver mes aliments substitués.
\nq. Quitter.
\nEntrer votre réponse: """

display_categories = """\nb. Retour
q. Quitter
\nSélectionnez une catégorie: """

display_products = """\nb. Retour
q. Quitter
\nSélectionnez un produit: """

display_chosen_substitute = """\nr. Enregistrer
b. Retour
q. Quitter
\nEntrez votre réponse: """

chosen_substitute = """\n********************\n
{}
Marque: {}
Point de vente: {}
Nutriscore: {}
{}\n
********************"""

display_substitutes = """\nb. Retour
q. Quitter
\nSélectionnez un substitut: """

display_login_menu = """\n----- INSCRIPTION - CONNEXION -----\n
1. Se connecter
2. S'inscrire
q. Quitter
\nSélectionnez une réponse: """

display_favorite_menu = """\nb. Retour
q. Quitter
\nEntrez votre réponse: """

display_favorites = """
{substitute}
Marque: {brand}
Point de vente: {store}
Nutriscore: {nutriscore}
Url: {url}
\n------------------------------------------------\n"""

valid_record = "\nLe produit est enregistré.\n"

information = """Retrouvez vos produits préférés dans la section :
[ Retrouver mes aliments substitués ]
Menu Principale > choix n°2"""

check = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

favorite = """
    SELECT
    product.name as substitute, brand, store.name as store, nutriscore, url
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
