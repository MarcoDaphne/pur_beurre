#!/usr/bin/env python
# Coding: utf-8

"""docstring"""

import re
from passlib.hash import argon2

import product_downloader as p_downloader
import constants as c


class ClientManager:
    def __init__(self, p_downloader):
        """ Constructor """
        self.p_downloader = p_downloader

    def check_email(self, email):
        match = re.match(c.check, email)
        if match is None:
            return True

    def check_email_database(self, email):
        """docstring"""
        list_email = self.p_downloader.db.query(c.list_email)
        list_email = list_email.as_dict()
        for dictionary in list_email:
            if email in dictionary.values():
                return True

    def check_password(self, email, password):
        """docstring"""
        list_password = self.p_downloader.db.query(
            c.check_password, email=email)
        list_password = list_password.as_dict()
        for dictionary in list_password:
            if argon2.verify(password, dictionary['password']):
                return True

    def get_id_client(self, email):
        """docstring"""
        id_client = self.p_downloader.db.query(c.id_client, email=email)
        id_client = id_client.as_dict()
        return id_client[0]['id']

    def register_client(self, email, password):
        """docstring"""
        return self.p_downloader.db.query(
            c.register_client,
            email=email,
            password=password)


if __name__ == "__main__":
    p_downloader = p_downloader.ProductDownloader()
    manage_client = ClientManager(p_downloader)
