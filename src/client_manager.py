#!/usr/bin/env python
# Coding: utf-8

"""docstring"""

import hashlib
from getpass import getpass

import product_downloader as pd
import constants as c


class ClientManager:
    def __init__(self, pd):
        """ Constructor """
        self.pd = pd

    def check_name(self, name):
        """docstring"""
        list_name = self.pd.db.query(c.list_name)
        list_name = list_name.as_dict()
        for dictionary in list_name:
            if name in dictionary.values():
                return True

    def check_password(self, name, password):
        """docstring"""
        list_password = self.pd.db.query(c.check_password, name=name)
        list_password = list_password.as_dict()
        for dictionary in list_password:
            if password == dictionary['password']:
                return True

    def sign_in(self):
        """docstring"""
        print("\n----- INSCRIPTION -----\n")
        not_registered = True
        while not_registered:
            name = input("Entrez votre pseudo: ")
            name = name.capitalize()
            if len(name) < 3:
                print("\n4 caractères minimum.\n")
            elif self.check_name(name) is True:
                print("'{}' existe déjà dans la base de donnée.".format(name))
            else:
                password = input("Entrez votre mot de passe: ")
                if len(password) < 5:
                    print("\n6 caractères minimum.\n")
                else:
                    password = "@Pur_Beurre" + password + "Sign_in@"
                    password = password.encode()
                    password = hashlib.sha1(password).hexdigest()
                    self.pd.db.query(
                        c.register_client,
                        name=name,
                        password=password)
                    not_registered = False
        print("\nBienvenue {} !!!\n".format(name))

    def login(self):
        """docstring"""
        print("\n----- CONNEXION -----\n")
        not_connected = True
        while not_connected:
            name = input("Pseudo: ")
            name = name.capitalize()
            if self.check_name(name) is not True:
                print("\n'{}' n'existe pas dans la base de donnée.\n".format(
                    name))
            else:
                password = getpass("Mot de passe: ")
                password = "@Pur_Beurre" + password + "Sign_in@"
                password = password.encode()
                password = hashlib.sha1(password).hexdigest()
                if self.check_password(name, password) is not True:
                    print("\nMot de passe incorrect.\n")
                else:
                    print("\nBonjour {} !!!\n".format(name))
                    not_connected = False


if __name__ == "__main__":
    pd = pd.ProductDownloader()
    manage_client = ClientManager(pd)
    manage_client.sign_in()
    manage_client.login()
