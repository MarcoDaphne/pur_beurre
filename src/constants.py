url = 'https://fr.openfoodfacts.org/cgi/search.pl'
connexion = "mysql+pymysql://testeur:camomille@localhost/test?charset=utf8mb4"
directory = "sql"
products = 'products'
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
rds_prod = """
    INSERT INTO
        product (code, name, brand, url, nutriscore)
    VALUES
        (:code, :name, :brand, :url, :nutriscore)"""
