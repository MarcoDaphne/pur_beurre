#!/usr/bin/env python
# Coding: utf-8

"""docstring"""


import product_downloader as prodl
import constants as c


class Interface:
    """docstring"""

    def __init__(self, prodl):
        """Constructor"""
        self.prodl = prodl

    def choose_category(self):
        categories = self.prodl.db.query(c.sel_cat)
        categories = categories.as_dict()
        for category in categories:
            print('{} - {}'.format(category['id'], category['name'].upper()))
        category_choice = int(input('\nSélectionnez une catégorie : '))
        return category_choice

    def choose_product(self):
        choice = self.choose_category()
        products = self.prodl.db.query(c.sel_prod, cat_id=choice)
        products = products.as_dict()
        identification = []
        for i, product in enumerate(products):
            i += 1
            print("\n{} - {}\n".format(i, product['name'].title()))
            print("Marque: {} ||| Point de vente: {} ||| Code: {}".format(
                product['brand'],
                product['store'],
                product['code']))
            print("Url: {}".format(product['url']))
            print("Nutriscore: {}\n\n\n".format(product['nutriscore'].upper()))
            identification.append((i, product['code']))
        product_choice = int(input('Sélectionner un produit : '))
        return product_choice, identification

    def want_record(self):
        choice, id_product = self.choose_product()
        for element in id_product:
            if choice == element[0]:
                show = self.prodl.db.query(c.product, cod=element[1])
                for i in show:
                    print("\n- {}".format(i['name'].title()))
                    print("Code : {}".format(i['code']))
                    print("Marque : {}".format(i['brand']))
                    print("Point de vente : {}".format(i['store']))
                    print("Nutriscore : {}".format(i['nutriscore'].upper()))
                    print("Url : {}".format(i['url']))


if __name__ == "__main__":
    prodl = prodl.ProductDownloader()
    client = Interface(prodl)
    client.want_record()
