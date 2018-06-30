#!/usr/bin/env python
# Coding: utf-8

"""This module responsible for retrieving
information related to categories in the database.
"""

import product_downloader as p_downloader


class CategoryManager:
    """This Class makes sql queries to get all categories."""

    def __init__(self, p_downloader):
        """Constructor

        Params:
            p_downloader: Instance of the Class ProductDownloader

        """
        self.p_downloader = p_downloader

    def get_categories(self):
        """Select from database the categories's id and
        the categories name on the database
        """
        datas = self.p_downloader.db.query("""
            SELECT *
            FROM category
            ORDER BY id
            """)
        datas = datas.as_dict()
        return datas


if __name__ == '__main__':
    p_downloader = p_downloader.ProductDownloader()
    manage_category = CategoryManager(p_downloader)
    manage_category.get_categories()
