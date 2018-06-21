#!/usr/bin/env python
# Coding: utf-8

import product_downloader as pd
import constants as c


class ProductManager:
    def __init__(self, pd):
        self.pd = pd

    def display_product(self, cat_id=int()):
        datas = self.pd.db.query(c.product, cat_id=cat_id)
        datas = datas.as_dict()
        print("\n----- PRODUITS -----\n")
        for i, dictionary in enumerate(datas):
            i += 1
            print("{}. {name}".format(i, **dictionary))

    def display_substitute(self, cat_id=int()):
        datas = self.pd.db.query(c.substitute, cat_id=cat_id)
        datas = datas.as_dict()
        list_id = []
        print("\n----- SUBSTITUTS -----\n")
        for i, dictionary in enumerate(datas):
            i += 1
            list_id.append((i, dictionary['code']))
            print("{}. {name}\n*** Nutriscore: {nutriscore} ***".format(
                i, **dictionary))
        return list_id

    def display_chosen_product(self, code=int()):
        datas = self.pd.db.query(c.chosen_product, code=code)
        datas = datas.as_dict()
        for dictionary in datas:
            print("\n----- {} -----\n".format(
                dictionary['substitute'].upper()))
            id_substitute = dictionary['code']
            print(c.chosen_substitute.format(**dictionary))
        return id_substitute


if __name__ == '__main__':
    pd = pd.ProductDownloader()
    manage_product = ProductManager(pd)
    manage_product.display_product()
    manage_product.display_substitute()
    manage_product.display_chosen_product()
