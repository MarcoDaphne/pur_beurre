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

    def format(self, line, category):
        """docstring"""
        for product in category:
            self.db.query(
                line,
                code=product['code'],
                name=product['product_name'],
                brand=product['brands'],
                nutriscore=product['nutrition_grade_fr'],
                url=product['url'])

    def insert_data(self):
        """docstring"""
        pizza = self.get_response(c.pizza, c.ngrad_d)
        burger = self.get_response(c.burger, c.ngrad_d)
        pat = self.get_response(c.pat, c.ngrad_d)
        glace = self.get_response(c.glace, c.ngrad_d)
        soda = self.get_response(c.soda, c.ngrad_d)
        insert = self.load(c.insert_data)
        with open(insert) as f:
            for line in f:
                self.format(line, pizza)
                self.format(line, burger)
                self.format(line, soda)
                self.format(line, pat)
                self.format(line, glace)


if __name__ == "__main__":
    downloader = ProductDownloader()
    downloader.create_table()
    downloader.insert_data()
