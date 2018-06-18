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

    def display_substitute_menu(self, code, num):
        chosen_product = self.product_manager.display_with_id(
            c.chosen_product, code)
        substitute = self.product_manager.display_by_category(
            c.substitute, num)
        list_id = []
        for dictionary in chosen_product:
            print('\n----- {} -----\n'.format(dictionary['product'].upper()))
            print(c.display_chosen_product.format(**dictionary))
        print('\n----- SUBSTITUTS -----\n')
        for i, dictionary in enumerate(substitute):
            i += 1
            list_id.append((i, dictionary['code']))
            print(c.display_substitutes.format(i, **dictionary))

    def display_product_menu(self, num):
        products = self.product_manager.display_by_category(c.product, num)
        list_id = []
        print('\n----- PRODUITS -----\n')
        for i, dictionary in enumerate(products):
            i += 1
            list_id.append((i, dictionary['code']))
            print(c.display_products.format(i, **dictionary))
        response = self.get_response("""\nb. Retour\nq. Quitter
\nEntrer votre réponse: """, "12345678910bq")
        next_step = {
            "1": self.display_substitute_menu,
            "2": self.display_substitute_menu,
            "3": self.display_substitute_menu,
            "4": self.display_substitute_menu,
            "5": self.display_substitute_menu,
            "6": self.display_substitute_menu,
            "7": self.display_substitute_menu,
            "8": self.display_substitute_menu,
            "9": self.display_substitute_menu,
            "10": self.display_substitute_menu,
            "b": self.display_category_menu,
            "q": self.quit_menu
        }
        if response in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            for element in list_id:
                if int(response) == element[0]:
                    next_step[response](element[1], num)
        else:
            next_step[response]()

    def display_category_menu(self):
        category = self.category_manager.select_category()
        response = self.get_response(c.display_categories.format(
            category[0]['id'], category[0]['name'].capitalize(),
            category[1]['id'], category[1]['name'].capitalize(),
            category[2]['id'], category[2]['name'].capitalize(),
            category[3]['id'], category[3]['name'].capitalize(),
            category[4]['id'], category[4]['name'].capitalize()),
            "12345bq")
        next_step = {
            "1": self.display_product_menu,
            "2": self.display_product_menu,
            "3": self.display_product_menu,
            "4": self.display_product_menu,
            "5": self.display_product_menu,
            "b": self.display_main_menu,
            "q": self.quit_menu
        }
        params = response
        if response in ['1', '2', '3', '4', '5']:
            params = int(response)
            next_step[response](params)
        else:
            next_step[response]()

    def quit_menu(self):
        return quit('A bientôt')

    def display_main_menu(self):
        response = self.get_response(c.display_menu, "1q")
        next_step = {
            "1": self.display_category_menu,
            "q": self.quit_menu
        }
        return next_step[response]()


if __name__ == "__main__":
    downloader = product_downloader.ProductDownloader()
    manager_c = category_manager.CategoryManager(downloader)
    manager_p = product_manager.ProductManager(downloader)
    client = Interface(downloader, manager_c, manager_p)
    client.display_main_menu()
