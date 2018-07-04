#!/usr/bin/env python
# Coding: utf-8

"""This module is responsible for launching the application"""


from passlib.hash import argon2
from getpass import getpass
import time

import product_downloader as product_d
import category_manager as category_m
import product_manager as product_m
import client_manager as client_m
import favorite_manager as favorite_m
import constants as c


class Interface:
    """docstring"""

    def __init__(self, product_d, category_m, product_m, client_m, favorite_m):
        """Constructor

        Params:
            product_d: Instance of the Class ProductDownloader
            category_m: Instance of the Class CategoryManager
            product_m: Instance of the Class ProductManager
            client_m: Instance of the Class ClientManager
            favorite_m: Instance of the Class FavoriteManager
        """
        self.product_d = product_d
        self.category_m = category_m
        self.product_m = product_m
        self.client_m = client_m
        self.favorite_m = favorite_m
        self.session = {'user': None, 'connected': False}

    def get_response(self, prompt, valid_response):
        """Ask the user a valid answer

        Check that there is no empty entry
        Check that the entry is valid based
        on a verification string

        Params:
            prompt (str()): User input
            valid_response (str()): Verification string
        """
        while True:
            response = input(prompt).strip()
            if response == "":
                print("\nRéponse non valide\n")
            elif response in valid_response:
                return response

    def valid_record(self):
        """Display messages to validate the registration
        of a substitute by pausing for three seconds
        """
        print(c.valid_record)
        time.sleep(3)
        print(c.information)
        time.sleep(3)

    def stop_authentication(self, response):
        """Return to the main menu or exit the application
        depending on the user's response

        Params:
            Response (str()): User's response
        """
        if response == 'm':
            self.display_main_menu()
        elif response == 'q':
            self.quit_menu()

    def sign_in(self):
        """Ask the user to enter his login details for sign in

        Ask the user to enter his email address
        Check the correspondence between the email address entered
        by the user and the syntax of a lambda email address
        Check that the email address does not exist on  the database
        Ask the user to enter his password
        Check the length of the user's password and encrypt the
        password before recording the email and password on the database
        The user can abort the registration procedure by
        returning to the main menu or exiting the application
        """
        print("\n****** INSCRIPTION ******\n")
        not_registered = True
        while not_registered:
            email = input(c.get_email)
            self.stop_authentication(email)
            if self.client_m.check_email(email) is True:
                print("\nAdresse email non valide.\n")
            elif self.client_m.check_email_database(email) is True:
                print("'{}' existe déjà dans la base de donnée.".format(email))
            else:
                password = input(c.get_password)
                self.stop_authentication(password)
                if len(password) < 5:
                    print("\n6 caractères minimum.\n")
                else:
                    password = argon2.hash(password)
                    self.client_m.register_client(email, password)
                    not_registered = False

    def log_in(self):
        """Ask the user to enter his login details for log in

        Ask the user to enter his email address
        Check that the email address exists in the database
        Ask the user to enter his password
        Check the correspondence between the email address
        and the password of the user on the database then
        change the values of the session dictionary so that
        the user is no longer to log in again.
        The user can abort the connection procedure by
        returning to the main menu or exiting the application
        """
        print("\n****** CONNEXION ******\n")
        while self.session['connected'] is False:
            email = input(c.ask_email)
            self.stop_authentication(email)
            if self.client_m.check_email_database(email) is not True:
                print("\n'{}' n'existe pas dans la base de donnée.\n".format(
                    email))
            else:
                password = getpass(c.ask_password)
                self.stop_authentication(password)
                if self.client_m.check_password(email, password) is not True:
                    print("\nMot de passe incorrect.\n")
                else:
                    self.session['user'] = email
                    self.session['connected'] = True
                    print("\nVous êtes connecté")

    def sign_in_then_log_in(self):
        """Execute the methods to register and connect"""
        self.sign_in()
        self.log_in()

    def log_in_menu(self, substitute_id, category_id):
        """Display the login menu and waits for the user's choice

        Ask the user to choose:
        1: Log in
        2: Sign in then Log in
        b: Back (Chosen substitute)
        q: Quit

        If the user wants to go back:
        Pass in parameter the product code and the number of the category
        chosen by the user for the next step (Chosen substitute)

        Params:
            substitute_id (int()): Product code
            category_id (int()): Number of the category chosen
        """
        response = self.get_response(c.display_login_menu, "12bq")
        next_step = {
            "1": self.log_in,
            "2": self.sign_in_then_log_in,
            "b": self.record_substitute_menu,
            "q": self.quit_menu
        }
        if response == "b":
            next_step[response](substitute_id, category_id)
        else:
            next_step[response]()

    def show_favorites(self, client_id):
        """Show favorites according to user's id

        Browse the list of favorite dictionaries,
        retrieve the product code to find the stores
        related to the favorite.
        Retrieve the values from the list of store dictionaries
        in a list that is then converted to a comma-separated
        character string (for displaying multiple stores
        for a favorite) and then displays all favorites
        and their descriptions

        Params:
            client_id (int()): User's id
        """
        favorites = self.favorite_m.retrieve_favorites(client_id)
        print("\n****** FAVORIS ******\n")
        for i, dictionary in enumerate(favorites):
            code = dictionary['code']
            store_names = self.favorite_m.retrieve_stores(code)
            store_names = [store['store']for store in store_names]
            stores = ", ".join(store_names)
            print(c.display_favorites.format(
                i=i + 1, stores=stores, **dictionary))

    def display_favorite_menu(self):
        """Display the favorites menu and waits for the user's choice

        Ask the user to choose:
        b: Back (Main menu)
        q: Quit

        If the user is not logged in, ask them to log in before
        displaying their favorites
        """
        if self.session['connected'] is False:
            self.log_in()
        id_client = self.client_m.get_id_client(self.session['user'])
        self.show_favorites(id_client)
        response = self.get_response(c.display_favorite_menu, "bq")
        next_step = {
            "b": self.display_main_menu,
            "q": self.quit_menu
        }
        next_step[response]()

    def show_chosen_substitute(self, substitute_id):
        """Show the description of the chosen substitute
        based on its product code

        Format the values of the list of dictionaries
        according to their keys to display them then
        return the product code

        params:
            substitute_id (int()): Product code
        """
        substitute = self.product_m.get_chosen_substitute(substitute_id)
        print("\n****** SUBSTITUT SELECTIONNE ******\n")
        print(c.chosen_substitute.format(
            substitute[0]['substitute'],
            substitute[0]['brand'],
            substitute[0]['store'],
            substitute[0]['nutriscore'],
            substitute[0]['url']))
        return substitute[0]['code']

    def record_substitute_menu(self, substitute_id, category_id):
        """Display substitute chosen menu and wait for the user's choice

        Ask the user to choose:
        r: Record the substitute in his favorites
        b: Back (Substitutes menu)
        m: Main menu
        q: Quit

        If the user chooses to record the substitute and is not connected:
        Pass the substitute id and the category chosen as a parameter for
        the next step (Sign in | Login + Check database + Record substitutes).
        Otherwise verify that the substitute does not exist
        in database, before recording the substitute in the favorites,
        display a registration validation message then go back to the
        substitutes menu
        And if the user chooses to go back:
        Pass the number of the category chosen as a parameter
        of next step (Substitutes menu)

        Params:
            substitute_id (int()): Product code
            category_id (int()): Number of the category
        """
        substitute_id = self.show_chosen_substitute(substitute_id)
        response = self.get_response(
            c.display_chosen_substitute, "rbmq")
        next_step = {
            "r": self.favorite_m.record_substitute,
            "b": self.display_substitute_menu,
            "m": self.display_main_menu,
            "q": self.quit_menu
        }
        if response == 'r':
            if self.session['connected'] is False:
                self.log_in_menu(substitute_id, category_id)
            id_client = self.client_m.get_id_client(self.session['user'])
            if self.favorite_m.check(substitute_id, id_client) is True:
                print("\nCe substitut a déjà été enregistré...")
                time.sleep(3)
                self.display_substitute_menu(category_id)
            next_step[response](id_client, substitute_id)
            self.valid_record()
            self.display_substitute_menu(category_id)
        elif response == 'b':
            next_step[response](category_id)
        else:
            next_step[response]()

    def show_substitutes(self, category_id):
        """Randomly Show five substitutes
        whose nutrition grade is between A and B,
        depending on which category the user has chosen

        Browse the list of dictionaries,
        number each dictionary, add each number and
        product code to a list, format the number
        and values of the dictionaries to display them
        then return the product code list.

        Params:
            category_id (int()): Number of the category
        """
        substitutes = self.product_m.get_substitutes(category_id)
        list_id = []
        print("\n****** SUBSTITUTS ******\n")
        for i, dictionary in enumerate(substitutes):
            list_id.append((i + 1, dictionary['code']))
            print("{}. {} - Nutriscore: [{}]".format(
                i + 1,
                dictionary['name'],
                dictionary['nutriscore']))
        return list_id

    def display_substitute_menu(self, category_id):
        """Display the substitute menu and wait for the user choice

        Ask the user to choose:
        between numbers 1 and 5: Substitutes
        b: Back (Products menu)
        m: Main menu
        q: Quit

        If the user chooses a substitute:
        Retrieves the product code of substitute from
        the product code list and passes it as a parameter
        of the next step (Chosen substitute menu)
        And if the user chooses to go back:
        Pass the number of the category chosen as a parameter
        of next step (Products menu)

        Params:
            category_id (int()): Number of the category
        """
        list_id = self.show_substitutes(category_id)
        response = self.get_response(c.display_substitutes, "12345bmq")
        next_step = {
            "1": self.record_substitute_menu,
            "2": self.record_substitute_menu,
            "3": self.record_substitute_menu,
            "4": self.record_substitute_menu,
            "5": self.record_substitute_menu,
            "b": self.display_product_menu,
            "m": self.display_main_menu,
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
        """Show ten products whose nutrition grade is
        between C and E, depending on which category
        the user has chosen

        Browse the list of dictionaries,
        number each dictionary then format the number
        and values of the dictionaries to display them.

        Params:
            category_id (int()): Number of the category
        """
        products = self.product_m.get_products(category_id)
        print("\n****** PRODUITS ******\n")
        for i, dictionary in enumerate(products):
            print("{}. {name}".format(i + 1, **dictionary))

    def display_product_menu(self, category_id):
        """Display the products menu and wait for the user choice

        Ask the user to choose:
        between numbers 1 and 10: Products
        b: Back (Categories menu)
        m: Main menu
        q: Quit

        If the user choose a product:
        Pass the number of the category chosen as a parameter
        of next step (display of substitutes)

        Params:
            category_id (int()): Number of the category
        """
        self.show_products(category_id)
        response = self.get_response(c.display_products, "12345678910bmq")
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
            "m": self.display_main_menu,
            "q": self.quit_menu
        }
        if response in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            next_step[response](category_id)
        else:
            next_step[response]()

    def show_categories(self):
        """Show all categories

        Browse the list of dictionaries then
        format the dictionaries values to display them.
        """
        categories = self.category_m.get_categories()
        print("\n****** CATEGORIES ******\n")
        for dictionary in categories:
            print("{}. {}".format(
                dictionary['id'],
                dictionary['name'].capitalize()))

    def display_category_menu(self):
        """Display the categories menu and wait the user's choice

        Ask the user to choose:
        Between numbers 1 and 5: Categories
        b: Back (main menu)
        q: Quit

        If the user choose a category:
        Pass the user's answer converted into a number
        as a parameter of the next step (product display)
        """
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
        """Leave the program

        Displays a message bye, pauses for 3 seconds
        and exits the program.
        """
        print('\nA bientôt')
        time.sleep(3)
        quit()

    def display_main_menu(self):
        """Display the main menu and wait for the user's choice

        Ask the user to choose:
        1: if he wants to search for products
        2: if he wants to find his registered substitutes
        q: Quit
        """
        response = self.get_response(c.display_menu, "12q")
        next_step = {
            "1": self.display_category_menu,
            "2": self.display_favorite_menu,
            "q": self.quit_menu
        }
        next_step[response]()


if __name__ == "__main__":
    admin = product_d.ProductDownloader()
    manage_cat = category_m.CategoryManager(admin)
    manage_prod = product_m.ProductManager(admin)
    manage_cli = client_m.ClientManager(admin)
    manage_fav = favorite_m.FavoriteManager(admin)
    client = Interface(admin, manage_cat, manage_prod, manage_cli, manage_fav)
    client.display_main_menu()
