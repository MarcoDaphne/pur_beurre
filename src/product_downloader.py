#!/usr/bin/env python
# coding: utf-8

"""docstring"""

import os

import requests
import records

import constants as c


class ProductDownloader:
    """docstring"""

    def __init__(self):
        """Constructor"""
        self.url = c.url
        self.db = records.Database(c.connexion)
        self.stores = []

    def get_response(self, category, nutrition_grade, number=20):
        """docstring"""
        parameters = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": nutrition_grade,
            "page_size": number,
            "json": "1"
        }
        response = requests.get(self.url, params=parameters)
        return response.json()[c.products]

    def load(self, file, sql=c.directory):
        """docstring"""
        directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path_to_file = os.path.join(directory, sql, file)
        return path_to_file

    def create_table(self):
        """docstring"""
        create = self.load(c.create_table)
        with open(create) as f:
            for line in f:
                self.db.query(line)

    def get_stores(self, stores):
        """docstring"""
        self.stores.append(stores)
        for store in self.stores:
            self.db.query(c.rds_store, name=store)

    def insert(self, products, category):
        """docstring"""
        self.db.query(c.rds_cat, name=category)
        for product in products:
            # -- Remplir la table store
            # Récupérer le champs product['stores']
            # Le transformer en une liste de magasins
            # Parcourir cette liste avec une boucle for
            # Insérer chaque element dans la la table
            # ON DUPLICATE KEY UPDATE name = :name
            self.db.query(
                c.rds_prod,
                code=product['code'],
                name=product['product_name'],
                brand=product['brands'],
                nutriscore=product['nutrition_grade_fr'],
                url=product['url'],
                cat_name=category)
            self.get_stores(product['stores'])

    def insert_data(self):
        """docstring"""
        for category in c.categories:
            data = self.get_response(category, c.ngrad_d)
            self.insert(data, category)


if __name__ == "__main__":
    downloader = ProductDownloader()
    downloader.create_table()
    downloader.insert_data()
