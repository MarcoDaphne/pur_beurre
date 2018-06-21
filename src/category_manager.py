#!/usr/bin/env python
# Coding: utf-8

import product_downloader as pd
import constants as c


class CategoryManager:
    def __init__(self, pd):
        self.pd = pd
        self.categories = []

    def display_category(self):
        datas = self.pd.db.query(c.category)
        datas = datas.as_dict()
        print("\n----- CATEGORIES -----\n")
        for dictionary in datas:
            print("{}. {}".format(
                dictionary['id'],
                dictionary['name'].capitalize()))


if __name__ == '__main__':
    pd = pd.ProductDownloader()
    manage_category = CategoryManager(pd)
    manage_category.display_category()
