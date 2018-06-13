#!/usr/bin/env python
# Coding: utf-8

import product_downloader as pd
import constants as c


class CategoryManager:
    def __init__(self, pd):
        self.pd = pd

    def select_category(self):
        categories = self.pd.db.query(c.category)
        categories = categories.as_dict()
        return categories


if __name__ == '__main__':
    pd = pd.ProductDownloader()
    manage_category = CategoryManager(pd)
    manage_category.select_category()
