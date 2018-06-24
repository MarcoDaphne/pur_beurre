#!/usr/bin/env python
# Coding: utf-8

import product_downloader as pd
import constants as c


class FavoriteManager:
    def __init__(self, pd):
        self.pd = pd

    def record_substitute(self, client=int(), code=int()):
        """docstring"""
        return self.pd.db.query(
            c.record_substitute,
            client_id=client,
            product_id=code)

    def retrieve_substitutes(self, client_id=int()):
        """docstring"""
        datas = self.pd.db.query(c.favorite, client=client_id)
        datas = datas.as_dict()
        return datas


if __name__ == '__main__':
    pd = pd.ProductDownloader()
    manage_favorite = FavoriteManager(pd)
    manage_favorite.record_substitute()
    manage_favorite.retrieve_substitutes()
