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

    def get_response(self, category, number=20):
        """docstring"""
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

    def get_stores(self, stores, product_code):
        """docstring"""
        if len(stores.strip()) != 0:
            list_store = stores.split(c.comma)
            for store in list_store:
                self.db.query(c.records_store, name=store)
                self.db.query(
                    c.records_store_product,
                    code=product_code,
                    store=store)

    def is_product_invalid(self, product):
        """docstring"""
        keys = ['code', 'product_name', 'nutrition_grade_fr', 'url']
        for key in keys:
            if key not in product or not product[key]:
                return True
        return False

    def insert(self, products, category):
        """docstring"""
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
        """docstring"""
        for category in c.categories:
            data = self.get_response(category, 1000)
            self.insert(data, category)


if __name__ == "__main__":
    downloader = ProductDownloader()
    downloader.create_table()
    downloader.insert_data()
