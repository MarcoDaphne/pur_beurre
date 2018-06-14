#!/usr/bin/env python
# Coding: utf-8

import product_downloader as pd
import constants as c


class ProductManager:
    def __init__(self, pd):
        self.pd = pd

    def select_product(self, num=int()):
        datas = self.pd.db.query(c.product, cat_id=num)
        datas = datas.as_dict()
        return datas


if __name__ == '__main__':
    pd = pd.ProductDownloader()
    manage_product = ProductManager(pd)
    manage_product.select_product()
