#!/usr/bin/env python
# Coding: utf-8

import webbrowser

import product_downloader as p_downloader
import constants as c


class FavoriteManager:
    def __init__(self, p_downloader):
        self.p_downloader = p_downloader

    def record_substitute(self, client=int(), code=int()):
        """docstring"""
        return self.p_downloader.db.query(
            c.record_substitute,
            client_id=client,
            product_id=code)

    def retrieve_substitutes(self, client_id=int()):
        """docstring"""
        datas = self.p_downloader.db.query(c.favorite, client=client_id)
        datas = datas.as_dict()
        return datas

    def show_page_web(self, url):
        webbrowser.open(url)


if __name__ == '__main__':
    p_downloader = p_downloader.ProductDownloader()
    manage_favorite = FavoriteManager(p_downloader)
    manage_favorite.record_substitute()
    manage_favorite.retrieve_substitutes()
