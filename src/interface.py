#!/usr/bin/env python
# Coding: utf-8

"""docstring"""


import product_downloader
import category_manager
import product_manager
import constants as c


class Interface:
    """docstring"""

    def __init__(self, product_downloader, category_manager, product_manager):
        """Constructor"""
        self.product_downloader = product_downloader
        self.category_manager = category_manager
        self.product_manager = product_manager

    def get_response(self, prompt, valid_response):
        while True:
            response = input(prompt).strip()
            if response in valid_response:
                return response

    def show_category(self):
        categories = self.category_manager.select_category()
        for category in categories:
            print('\t{}. {}'.format(category['id'], category['name']))
        self.submenu1()

    def show_products(self):
        products = self.product_manager.select_product()
        identification = []
        for i, product in enumerate(products):
            i += 1
            print("\n{} - {}\n".format(i, product['name'].title()))
            print("Marque: {} ||| Point de vente: {} ||| Code: {}".format(
                product['brand'],
                product['store'],
                product['code']))
            print("Url: {}".format(product['url']))
            print("Nutriscore: {}\n\n\n".format(product['nutriscore'].upper()))
            identification.append((i, product['code']))
        product_choice = int(input('Sélectionner un produit : '))
        return product_choice, identification

    def want_record(self):
        for element in id_product:
            if choice == element[0]:
                show = self.prodl.db.query(c.product, cod=element[1])
                for i in show:
                    print("\n- {}".format(i['name'].title()))
                    print("Code : {}".format(i['code']))
                    print("Marque : {}".format(i['brand']))
                    print("Point de vente : {}".format(i['store']))
                    print("Nutriscore : {}".format(i['nutriscore'].upper()))
                    print("Url : {}".format(i['url']))

    def main_menu(self):
        response = self.get_response("""--- Menu ---\n
1. Quel aliment souhaitez-vous remplacer ?
2. Retrouver mes aliments substitués.
q. Quitter.
\nEntrer votre réponse: """, "12q")
        next_step = {
            "1": self.submenu1(),
            "q": exit()
        }
        return next_step[response]()

    def submenu1(self):
        categories = self.category_manager.select_category()
        response = self.get_response("""\n---Catégories\n
{}. {}\n{}. {}\n{}. {}\n{}. {}\n{}. {}
b. Retour
q. Quitter
\nEntrer votre réponse: """.format(
            categories[0]['id'], categories[0]['name'].capitalize(),
            categories[1]['id'], categories[1]['name'].capitalize(),
            categories[2]['id'], categories[2]['name'].capitalize(),
            categories[3]['id'], categories[3]['name'].capitalize(),
            categories[4]['id'], categories[4]['name'].capitalize()), "12345bq")


if __name__ == "__main__":
    downloader = product_downloader.ProductDownloader()
    manager_c = category_manager.CategoryManager(downloader)
    manager_p = product_manager.ProductManager(downloader)
    client = Interface(downloader, manager_c, manager_p)
    client.main_menu()
