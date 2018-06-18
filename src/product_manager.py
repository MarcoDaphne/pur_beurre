#!/usr/bin/env python
# Coding: utf-8

import product_downloader as pd
import constants as c


class ProductManager:
    def __init__(self, pd):
        self.pd = pd

    def display_by_category(self, command=str(), num=int()):
        datas = self.pd.db.query(command, cat_id=num)
        datas = datas.as_dict()
        return datas

    def display_with_id(self, command=str(), code=int()):
        datas = self.pd.db.query(command, identification=code)
        datas = datas.as_dict()
        return datas


if __name__ == '__main__':
    pd = pd.ProductDownloader()
    manage_product = ProductManager(pd)
    manage_product.display_by_category()
    manage_product.display_with_id()
