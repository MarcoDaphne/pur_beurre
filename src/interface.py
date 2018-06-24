#!/usr/bin/env python
# Coding: utf-8

"""docstring"""


from passlib.hash import argon2
from getpass import getpass
import time

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

    def valid_record(self):
        print(c.valid_record)
        time.sleep(4)

    def sign_in(self):
        """docstring"""
        print("\n----- INSCRIPTION -----\n")
        not_registered = True
        while not_registered:
            email = input("Entrez votre email: ")
            if len(email) < 3:
                print("\n4 caractères minimum.\n")
            elif self.client_manager.check_email_database(email) is True:
                print("'{}' existe déjà dans la base de donnée.".format(email))
            else:
                password = input("Entrez votre mot de passe: ")
                if len(password) < 5:
                    print("\n6 caractères minimum.\n")
                else:
                    password = argon2.hash(password)
                    self.client_manager.register_client(email, password)
                    not_registered = False
                    print()

    def log_in(self):
        """docstring"""
        print("\n----- CONNEXION -----\n")
        while self.session['connected'] is False:
            email = input("Email: ")
            if self.client_manager.check_email_database(email) is not True:
                print("\n'{}' n'existe pas dans la base de donnée.\n".format(
                    email))
            else:
                password = getpass("Mot de passe: ")
                if self.client_manager.check_password(email,password) is not True:
                    print("\nMot de passe incorrect.\n")
                else:
                    self.session['user'] = email
                    self.session['connected'] = True
                    print("\nVous êtes connecté")

    def sign_in_then_log_in(self):
        """docstring"""
        self.sign_in()
        self.log_in()

    def log_in_menu(self):
        """docstring"""
        response = self.get_response(c.display_login_menu, "12q")
        next_step = {
            "1": self.log_in,
            "2": self.sign_in_then_log_in,
            "q": self.quit_menu
        }
        if response == "1":
            next_step[response]()
        elif response == "2":
            next_step[response]()
        else:
            next_step[response]()

    def show_favorites(self, client_id):
        """docstring"""
        substitutes = self.favorite_manager.retrieve_substitutes(client_id)
        print("\n------ SUBSTITUTS ENREGISTRES ------\n")
        for dictionary in substitutes:
            print(c.display_favorites.format(**dictionary))

    def display_favorite_menu(self):
        if self.session['connected'] is False:
            self.log_in_menu()
            id_client = self.client_manager.get_id_client(
                self.session['user'])
            self.show_favorites(id_client)
        else:
            id_client = self.client_manager.get_id_client(
                self.session['user'])
            self.show_favorites(id_client)
        response = self.get_response(c.display_favorite_menu, "bq")
        next_step = {
            "b": self.display_main_menu,
            "q": self.quit_menu
        }
        next_step[response]()

    def show_chosen_substitute(self, code):
        substitute = self.product_manager.get_chosen_substitute(code)
        print("\n------ SUBSTITUT CHOISI ------\n")
        print(c.chosen_substitute.format(
            substitute[0]['substitute'],
            substitute[0]['brand'],
            substitute[0]['store'],
            substitute[0]['nutriscore'],
            substitute[0]['url']))
        return substitute[0]['code']

    def record_substitute_menu(self, substitute_id, category_id):
        """docstring"""
        code = self.show_chosen_substitute(substitute_id)
        response = self.get_response(
            c.display_chosen_substitute, "rq")
        next_step = {
            "r": self.favorite_manager.record_substitute,
            "q": self.quit_menu
        }
        if response == 'r':
            if self.session['connected'] is False:
                self.log_in_menu()
                id_client = self.client_manager.get_id_client(
                    self.session['user'])
                next_step[response](id_client, code)
                self.valid_record()
                self.display_substitute_menu(category_id)
            else:
                id_client = self.client_manager.get_id_client(
                    self.session['user'])
                next_step[response](id_client, code)
                self.valid_record()
                self.display_substitute_menu(category_id)
        else:
            next_step[response]()

    def show_substitutes(self, category_id):
        """docstring"""
        substitutes = self.product_manager.get_substitutes(category_id)
        list_id = []
        print("\n------ SUBSTITUTS ------\n")
        for i, dictionary in enumerate(substitutes):
            i += 1
            list_id.append((i, dictionary['code']))
            print("{}. {} - Nutriscore: [{}]".format(
                i,
                dictionary['name'],
                dictionary['nutriscore']))
        return list_id

    def display_substitute_menu(self, category_id):
        """docstring"""
        list_id = self.show_substitutes(category_id)
        response = self.get_response(c.display_substitutes, "12345bq")
        next_step = {
            "1": self.record_substitute_menu,
            "2": self.record_substitute_menu,
            "3": self.record_substitute_menu,
            "4": self.record_substitute_menu,
            "5": self.record_substitute_menu,
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

    def show_products(self, category_id):
        """docstring"""
        products = self.product_manager.get_products(category_id)
        print("\n------ PRODUITS ------\n")
        for i, dictionary in enumerate(products):
            i += 1
            print("{}. {name}".format(i, **dictionary))

    def display_product_menu(self, category_id):
        """docstring"""
        self.show_products(category_id)
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

    def show_categories(self):
        """docstring"""
        categories = self.category_manager.get_categories()
        print("\n------ CATEGORIES ------\n")
        for dictionary in categories:
            print("{}. {}".format(
                dictionary['id'],
                dictionary['name'].capitalize()))

    def display_category_menu(self):
        """docstring"""
        self.show_categories()
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
        """docstring"""
        print('\nA bientôt')
        time.sleep(3)
        return quit()

    def display_main_menu(self):
        """docstring"""
        response = self.get_response(c.display_menu, "12q")
        next_step = {
            "1": self.display_category_menu,
            "2": self.display_favorite_menu,
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