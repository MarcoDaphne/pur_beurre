#!/usr/bin/env python
# Coding: utf-8

"""This module is responsible for verifying
authenticity before and after insertion and
inserting information into the database.
"""

import re
from passlib.hash import argon2

import product_downloader as p_downloader
import constants as c


class ClientManager:
    """This Class makes sql queries to check the email address
    syntax before insertion, the presence of the email address in database,
    the correspondence between user password and user email address
    in database, retrieves the user id and inserts the user
    identification information in database.
    """

    def __init__(self, p_downloader):
        """Constructor

        Params:
            p_downloader: Instance of the class ProductDownloader"""
        self.p_downloader = p_downloader

    def check_email(self, email):
        """Check the user email address syntax

        Params:
            email (str()): User email address
        """
        match = re.match(c.check, email)
        if match is None:
            return True

    def check_email_database(self, email):
        """Check the presence of the user email address in database

        Params:
            email (str()): User email address
        """
        list_email = self.p_downloader.db.query("""
                SELECT email
                FROM client
                """)
        list_email = list_email.as_dict()
        for dictionary in list_email:
            if email in dictionary.values():
                return True

    def check_password(self, email, password):
        """Check the correspondence between user password
        and user address email in database

        Params:
            email(str()): User email address
            password (str()): User password
        """
        list_password = self.p_downloader.db.query("""
                SELECT password
                FROM client
                WHERE email = :email
                """, email=email)
        list_password = list_password.as_dict()
        for dictionary in list_password:
            if argon2.verify(password, dictionary['password']):
                return True

    def get_id_client(self, email):
        """Select from database the user id according to
        the user email address

        Params:
            email (str()): User email address
        """
        id_client = self.p_downloader.db.query("""
                SELECT id
                FROM client
                WHERE email = :email
                """, email=email)
        id_client = id_client.as_dict()
        return id_client[0]['id']

    def register_client(self, email, password):
        """Insert into database the user email address and password

        Params:
            email (str()): User email address
            password (str()): User password
        """
        self.p_downloader.db.query("""
            INSERT INTO client (email, password)
            VALUES (:email, :password)
            ON DUPLICATE KEY UPDATE email = :email
            """, email=email, password=password)


if __name__ == "__main__":
    p_downloader = p_downloader.ProductDownloader()
    manage_client = ClientManager(p_downloader)
