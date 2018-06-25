#!/usr/bin/env python
# Coding: utf-8

import product_downloader as p_downloader
import constants as c


class CategoryManager:
    def __init__(self, p_downloader):
        self.p_downloader = p_downloader

    def get_categories(self):
        datas = self.p_downloader.db.query(c.category)
        datas = datas.as_dict()
        return datas


if __name__ == '__main__':
    p_downloader = p_downloader.ProductDownloader()
    manage_category = CategoryManager(p_downloader)
    manage_category.get_categories()
