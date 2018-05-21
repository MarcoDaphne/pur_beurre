#!/usr/bin/env python
# coding: utf-8

"""docstring"""

import requests
import records

import constants as c


class ProductDownloader:
    """docstring"""

    def __init__(self):
        """Constructor"""
        self.url = c.url
        self.db = records.Database(c.id_connexion)

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

    def data_insert(self, category, nutrition_grade):
        """docstring"""
        products = self.get_response(category, nutrition_grade)
        sql = """
            INSERT INTO
                product_list (id, name, brand, nutriscore, url)
            VALUES
                (:code, :name, :brand, :nutriscore, :url)"""
        for product in products:
            self.db.query(
                sql,
                code=product['code'],
                name=product['product_name'],
                brand=product['brands'],
                nutriscore=product['nutrition-score-fr'],
                url=product['url'])


if __name__ == "__main__":
    downloader = ProductDownloader()
    downloader.data_insert('pizza', 'D')
