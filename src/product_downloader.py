#!/usr/bin/env python
# coding: utf-8

"""This module is responsible for downloading the data and
storing it in the database.
"""

import os

import requests
import records

import constants as c


class ProductDownloader:
    """This class retrieves the data
    according to five categories,
    create the tables of the database
    and then store the data in database.
    """

    def __init__(self):
        """Constructor"""
        self.url = c.url
        self.db = records.Database(c.connexion)

    def get_response(self, category, number=20):
        """Make a GET request on Open Food Facts url
        and then return the products data in JSON format.

        Params:
            category (str()): Category of products
            number (int()): Number of products to recover
        """
        parameters = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "page_size": number,
            "json": "1"
        }
        response = requests.get(self.url, params=parameters)
        return response.json()['products']

    def load(self, file, sql="sql"):
        """Access a file in a folder that is in the parent
        folder of the module then return the path to the file.

        Params:
            file: The file used
            sql: The folder where the file is located
        """
        directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_file = os.path.join(directory, sql, file)
        return path_to_file

    def create_table(self):
        """Create tables in the database.

        Browse each line of the file after opening it
        and execute the sql commands.
        """
        create = self.load("create_table.sql")
        with open(create) as f:
            for line in f:
                self.db.query(line)

    def get_stores(self, stores, product_code):
        """Retrieve the stores to add them to the database.

        Check that the string is not empty.
        Add each store to a comma-separated list.
        Browse the list of stores and add them to the database.

        Params:
            stores: Product stores
            product_code: Product code
        """
        if len(stores.strip()) != 0:
            list_store = stores.split(',')
            for store in list_store:
                self.db.query(c.records_store, name=store)
                self.db.query(
                    c.records_store_product,
                    code=product_code,
                    store=store)

    def is_product_invalid(self, product):
        """Check existence of product data

        Browse a list of keys, verify that
        the key or value is present.

        Params:
            product: Product
        """
        keys = ['code', 'product_name', 'nutrition_grade_fr', 'url']
        for key in keys:
            if key not in product or not product[key]:
                return True
        return False

    def insert(self, products, category):
        """Define the categories, stores, key information
        to add to the database by making the necessary checks.

        Params:
            products: Products in Open Food Facts
            category: Category of products
        """
        self.db.query(c.records_category, name=category)
        for product in products:
            if self.is_product_invalid(product):
                continue
            self.db.query(
                c.records_product,
                code=product['code'],
                name=product['product_name'],
                brand=product.get('brands', ''),
                nutriscore=product['nutrition_grade_fr'],
                url=product['url'],
                cat_name=category)
            self.get_stores(product.get('stores', ''), product['code'])

    def insert_data(self):
        """Insert in the database the product data for each category"""
        for category in c.categories:
            data = self.get_response(category, 1000)
            self.insert(data, category)


if __name__ == "__main__":
    downloader = ProductDownloader()
    downloader.create_table()
    downloader.insert_data()
