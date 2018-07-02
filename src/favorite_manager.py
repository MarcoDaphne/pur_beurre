#!/usr/bin/env python
# Coding: utf-8

"""This module is responsible for inserting and
retrieving information related to the favorites in the database.
"""

import product_downloader as p_downloader


class FavoriteManager:
    """This Class makes sql queries to register substitutes
    according to the user's choice and find all registered substitutes.
    """

    def __init__(self, p_downloader):
        """Constructor

        Params:
            p_downloader: Instance of the Class ProductDownloader

        """
        self.p_downloader = p_downloader

    def record_substitute(self, client=int(), code=int()):
        """Insert into database the user's id
        and the product code of the substitute chosen

        Params:
            client: User id number
            code: Product code number

        """
        self.p_downloader.db.query("""
                INSERT INTO favorite (client_id, product_id)
                VALUES (:client_id, :product_id)
                """, client_id=client, product_id=code)

    def retrieve_stores(self, code=int()):
        datas = self.p_downloader.db.query("""
                SELECT store.name as store
                FROM store
                INNER JOIN store_product
                ON store_id = store.id
                INNER JOIN product
                ON product_code = product.code
                WHERE product.code = :code
                """, code=code)
        datas = datas.all(as_dict=True)
        return datas

    def retrieve_favorites(self, client_id=int()):
        """Select from database the name, brand,
        store, nutriscore, url of the favorite
        according to the user id

        Params:
            client_id: User id number"""
        datas = self.p_downloader.db.query("""
                SELECT product.code, product.name as favorite,
                brand, nutriscore, url
                FROM product
                INNER JOIN favorite
                ON product_id = product.code
                INNER JOIN client
                ON client.id = favorite.client_id
                WHERE client.id = :client
                """, client=client_id)
        datas = datas.all(as_dict=True)
        return datas


if __name__ == '__main__':
    p_downloader = p_downloader.ProductDownloader()
    manage_favorite = FavoriteManager(p_downloader)
    manage_favorite.record_substitute()
    manage_favorite.retrieve_substitutes()
    manage_favorite.test()
