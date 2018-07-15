url = 'https://fr.openfoodfacts.org/cgi/search.pl'

connexion = (
    "mysql+mysqlconnector://root:root@localhost/pur_beurre_p5?charset=utf8mb4")

categories = [
    'Charcuterie',
    'Fromage',
    'Steack',
    'Pizza',
    'Crème Glacée']

########################

records_product = """
    INSERT INTO
        product (code, name, brand, url, nutriscore, category_id)
    VALUES
        (:code, :name, :brand, :url, :nutriscore,
        (SELECT id FROM category WHERE name = :cat_name))
    ON DUPLICATE KEY UPDATE code = :code"""

records_category = """
    INSERT INTO
        category (name)
    VALUES
        (:name)"""

records_store = """
    INSERT INTO
        store (name)
    VALUES
        (:name)
    ON DUPLICATE KEY UPDATE name = :name"""

records_store_product = """
    INSERT INTO
        store_product (store_id, product_code)
    VALUES
        ((SELECT id FROM store WHERE name = :store), :code)"""

########################

display_menu = """\n****** MENU PRINCIPAL ******\n
1. Quel aliment souhaitez-vous remplacer ?
2. Retrouver mes aliments substitués.
\nq. Quitter.
\nEntrer votre réponse: """

display_categories = """\nb. Retour\tq. Quitter
\nSélectionnez une catégorie: """

display_products = """\nb. Retour\tm. Menu Principal\tq. Quitter
\nSélectionnez un produit: """

display_chosen_substitute = """r. Enregistrer
\nb. Retour\tm. Menu Principal\tq. Quitter
\nEntrez votre réponse: """

chosen_substitute = """{}
Marque: {}
Point de vente: {}
Nutriscore: {}
{}\n
"""

display_substitutes = """\nb. Retour\tm. Menu Principal\tq. Quitter
\nSélectionnez un substitut: """

display_login_menu = """\n****** INSCRIPTION - CONNEXION ******\n
1. Se connecter
2. S'inscrire
\nb. Retour\tq. Quitter
\nSélectionnez une réponse: """

display_favorite_menu = """\nb. Retour\tq. Quitter
\nEntrez votre réponse: """

get_email = """\nm. Menu Principal\tq. Quitter
\nEntrez votre e-mail: """

get_password = """\nm. Menu Principal\tq. Quitter
\nEntrez votre mot de passe: """

ask_email = """\nm. Menu Principal\tq. Quitter
\nE-mail: """

ask_password = """\nm. Menu Principal\tq. Quitter
\nMot de passe: """

display_favorites = """
{i}. {favorite}
Marque: {brand}
Nutriscore: {nutriscore}
Point de vente: {stores}
Url: {url}
\n_______________________\n"""

valid_record = "\nLe produit est enregistré.\n"

information = """Retrouvez vos produits préférés dans la section :
[ Retrouver mes aliments substitués ]
Menu Principal > choix n°2"""

check = (
    r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')
