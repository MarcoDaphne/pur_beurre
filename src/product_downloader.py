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
        return response.json()['products']

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

    def insert(self, products):
        """docstring"""
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
                url=product['url'])

    def insert_data(self):
        """docstring"""
        cat1 = self.get_response(c.cat1, c.ngrad_d)
        cat2 = self.get_response(c.cat2, c.ngrad_d)
        cat3 = self.get_response(c.cat3, c.ngrad_d)
        cat4 = self.get_response(c.cat4, c.ngrad_d)
        cat5 = self.get_response(c.cat5, c.ngrad_d)
        self.insert(cat1)
        self.insert(cat2)
        self.insert(cat3)
        self.insert(cat4)
        self.insert(cat5)


if __name__ == "__main__":
    downloader = ProductDownloader()
    downloader.create_table()
    downloader.insert_data()
