#!/usr/bin/env python
# Coding: utf-8

"""docstring"""


import product_downloader
import category_manager
import product_manager
import client_manager
import favorite_manager
import constants as c


class Interface:
    """docstring"""

    def __init__(
        self,
        product_downloader,
        category_manager,
        product_manager,
        client_manager,
        favorite_manager):
        """Constructor"""
        self.product_downloader = product_downloader
        self.category_manager = category_manager
        self.product_manager = product_manager
        self.client_manager = client_manager
        self.favorite_manager = favorite_manager
        self.session = {'user': None, 'connected': False}

    def get_response(self, prompt, valid_response):
        while True:
            response = input(prompt).strip()
            if response in valid_response:
                return response

    def log_in_menu(self, id_substitute, code, category_id):
        response = self.get_response(c.display_login_menu, "12bq")
        next_step = {
            "1": self.client_manager.log_in,
            "2": self.client_manager.sign_in_then_log_in,
            "b": self.chosen_substitute,
            "q": self.quit_menu
        }
        if response == "1":
            next_step[response]()
            id_client = self.client_manager.id_client
            self.favorite_manager.record_substitute(id_client, id_substitute)
            self.display_main_menu()
        elif response == "2":
            next_step[response]()
            id_client = self.client_manager.id_client
            self.favorite_manager.record_substitute(id_client, id_substitute)
            self.display_main_menu()
        elif response == "b":
            next_step[response](code, category_id)
        else:
            next_step[response]()

    def chosen_substitute(self, code, category_id):
        id_substitute = self.product_manager.display_chosen_product(code)
        response = self.get_response(
            c.display_chosen_substitute, "rbq")
        next_step = {
            "r": self.log_in_menu,
            "b": self.display_substitute_menu,
            "q": self.quit_menu
        }
        if response == 'r':
            next_step[response](id_substitute, code, category_id)
        elif response == 'b':
            next_step[response](category_id)
        else:
            next_step[response]()

    def display_substitute_menu(self, category_id):
        list_id = self.product_manager.display_substitute(category_id)
        response = self.get_response(c.display_substitutes, "12345bq")
        next_step = {
            "1": self.chosen_substitute,
            "2": self.chosen_substitute,
            "3": self.chosen_substitute,
            "4": self.chosen_substitute,
            "5": self.chosen_substitute,
            "b": self.display_product_menu,
            "q": self.quit_menu
        }
        if response in ['1', '2', '3', '4', '5']:
            for element in list_id:
                if int(response) == element[0]:
                    next_step[response](element[1], category_id)
        elif response == 'b':
            next_step[response](category_id)
        else:
            next_step[response]()

    def display_product_menu(self, category_id):
        self.product_manager.display_product(category_id)
        response = self.get_response(c.display_products, "12345678910bq")
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
            next_step[response](category_id)
        else:
            next_step[response]()

    def display_category_menu(self):
        """docstring"""
        self.category_manager.display_category()
        response = self.get_response(c.display_categories, "12345bq")
        next_step = {
            "1": self.display_product_menu,
            "2": self.display_product_menu,
            "3": self.display_product_menu,
            "4": self.display_product_menu,
            "5": self.display_product_menu,
            "b": self.display_main_menu,
            "q": self.quit_menu
        }
        if response in ['1', '2', '3', '4', '5']:
            category_id = int(response)
            next_step[response](category_id)
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
    manager_cat = category_manager.CategoryManager(downloader)
    manager_p = product_manager.ProductManager(downloader)
    manage_cli = client_manager.ClientManager(downloader)
    manage_fav = favorite_manager.FavoriteManager(downloader)
    client = Interface(downloader, manager_cat, manager_p, manage_cli, manage_fav)
    client.display_main_menu()
