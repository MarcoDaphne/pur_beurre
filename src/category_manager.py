#!/usr/bin/env python
# Coding: utf-8

import product_downloader as pd
import constants as c


class CategoryManager:
    def __init__(self, pd):
        self.pd = pd

    def get_categories(self):
        datas = self.pd.db.query(c.category)
        datas = datas.as_dict()
        return datas


if __name__ == '__main__':
    pd = pd.ProductDownloader()
    manage_category = CategoryManager(pd)
    manage_category.get_categories()
