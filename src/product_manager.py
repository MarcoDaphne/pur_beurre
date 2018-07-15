#!/usr/bin/env python
# Coding: utf-8

"""This module responsible for retrieving
product-related information from the database.
"""

import product_downloader as p_downloader


class ProductManager:
    """This Class makes sql queries to get
    ten products, five substitutes and
    the substitute chosen, depending on the
    user's choice.
    """

    def __init__(self, p_downloader):
        """Constructor

        Params:
            p_downloader: Instance of the Class ProductDownloader

        """
        self.p_downloader = p_downloader

    def get_products(self, cat_id=int()):
        """Select from database the product name
        according to chosen category
        whose nutrition grade is between C and E
        then return them in a dictionaries list

        Params:
            cat_id: Number of the products's category
        """
        datas = self.p_downloader.db.query("""
                SELECT name
                FROM product
                WHERE category_id = :cat_id
                AND nutriscore
                BETWEEN 'C' AND 'E'
                LIMIT 10
                """, cat_id=cat_id)
        datas = datas.as_dict()
        return datas

    def get_substitutes(self, cat_id=int()):
        """Select from database the code, name, and nutriscore
        of the product according to chosen category
        whose nutrition grade is between A and B
        then return them in a dictionaries list

        Params:
            cat_id: Number of the products's category
        """
        datas = self.p_downloader.db.query("""
                SELECT code, name, nutriscore
                FROM product
                WHERE category_id = :cat_id
                AND nutriscore
                BETWEEN 'A' AND 'B'
                ORDER BY RAND()
                LIMIT 5
                """, cat_id=cat_id)
        datas = datas.as_dict()
        return datas

    def get_chosen_substitute(self, code=int()):
        """Select from database the code, name, brand
        store, nutriscore and url of a product accordind to
        the product's code then returns it in a dictionary list

        Params:
            code: Product's code
        """
        datas = self.p_downloader.db.query("""
                SELECT code, name, brand, nutriscore, url
                FROM product
                WHERE product.code = :code
                """, code=code)
        datas = datas.as_dict()
        return datas


if __name__ == '__main__':
    p_downloader = p_downloader.ProductDownloader()
    manage_product = ProductManager(p_downloader)
    manage_product.get_products()
    manage_product.get_substitutes()
    manage_product.get_chosen_substitute()
