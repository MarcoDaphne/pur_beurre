#!/usr/bin/env python
# Coding: utf-8

"""docstring"""

from passlib.hash import argon2
from getpass import getpass

import product_downloader as pd
import constants as c


class ClientManager:
    def __init__(self, pd):
        """ Constructor """
        self.pd = pd
        self.id_client = int()

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
            if argon2.verify(password, dictionary['password']):
                return True

    def get_id_client(self, name):
        """docstring"""
        id_client = self.pd.db.query(c.id_client, name=name)
        id_client = id_client.as_dict()
        return id_client[0]['id']

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
                    password = argon2.hash(password)
                    self.pd.db.query(
                        c.register_client,
                        name=name,
                        password=password)
                    not_registered = False
        print("\nBienvenue {} !!!\n".format(name))

    def log_in(self):
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
                if self.check_password(name, password) is not True:
                    print("\nMot de passe incorrect.\n")
                else:
                    print("\nVous êtes connecté")
                    not_connected = False
        self.id_client = self.get_id_client(name)

    def sign_in_then_log_in(self):
        """docstring"""
        self.sign_in()
        self.log_in()


if __name__ == "__main__":
    pd = pd.ProductDownloader()
    manage_client = ClientManager(pd)
    manage_client.sign_in()
    manage_client.log_in()
    manage_client.sign_in_then_log_in()
