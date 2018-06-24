#!/usr/bin/env python
# Coding: utf-8

import product_downloader as pd
import constants as c


class ProductManager:
    def __init__(self, pd):
        self.pd = pd

    def get_products(self, cat_id=int()):
        datas = self.pd.db.query(c.product, cat_id=cat_id)
        datas = datas.as_dict()
        return datas

    def get_substitutes(self, cat_id=int()):
        datas = self.pd.db.query(c.substitute, cat_id=cat_id)
        datas = datas.as_dict()
        return datas

    def get_chosen_substitute(self, code=int()):
        datas = self.pd.db.query(c.chosen_product, code=code)
        datas = datas.as_dict()
        return datas


if __name__ == '__main__':
    pd = pd.ProductDownloader()
    manage_product = ProductManager(pd)
    manage_product.get_products()
    manage_product.get_substitutes()
    manage_product.get_chosen_substitute()
