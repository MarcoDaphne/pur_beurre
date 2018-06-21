#!/usr/bin/env python
# Coding: utf-8

import product_downloader as pd
import constants as c


class FavoriteManager:
    def __init__(self, pd):
        self.pd = pd

    def record_substitute(self, client=int(), code=int()):
        self.pd.db.query(
            c.r_substitute,
            c_id=client,
            p_id=code)
        print("\nLe substitut a été enregistré dans vos favoris.")


if __name__ == '__main__':
    pd = pd.ProductDownloader()
    manage_favorite = FavoriteManager(pd)
    manage_favorite.record_substitute()
