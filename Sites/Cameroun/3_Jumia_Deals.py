from bs4 import BeautifulSoup
import requests
from DataInsertion.database import  insertProduct

"""Fontion pour récupérer les urls de toutes les catégories """

def categoryJumiaDeals():

    site = 'https://deals.jumia.cm/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")
    category = page_content.find('ul',{"class":"list-group"}).findAll("li",{"class":"list-group-item"})

    categories_urls = []

    for item in category:
        urlCategory = site + item.find('a').get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls

#print(categoryJumiaDeals())


"""Fonction pour récupérer les noms et les urls de toutes les sous-catégories et les stocke dans une variable"""

def subCategoryJumiaDeals():

    categories_urls = categoryJumiaDeals()
    subUrl = []

    site = 'https://deals.jumia.cm'

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('nav', {"class": "category-links"}).findAll('li')

        for item in subCategories:
            subCategoryUrl = site + item.find('a').get("href")

            subUrl.append(
                subCategoryUrl
            )

    return subUrl

#print(subCategoryJumiaDeals())


def getAllPage():
    subUrl = subCategoryJumiaDeals()
    page = []

    for url in subUrl:
        try:
            maxPage = 9
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url + "?page=" + str(el)

                page.append({
                    'url': link
                })
        except:
            continue

    return page

#print(getAllPage())


def scrapJumiaDeals(origin):
    site = 'https://deals.jumia.cm/'
    page = getAllPage()
    produits = []

    for link in page:
        page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        logo = 'http://137.74.199.121/img/logo/gh/jumiadeals.jpg'
        logoS = 'http://137.74.199.121/img/logo/gh/logoS/jumiadeals.jpg'

        annonce = page_content.find_all("div", {"class": "post"})


        for item in annonce:
            try:
                url = item.findAll('a', {"class": "post-link"})[0].get("href")
                lib = item.find_all("a", {"class": "post-link"})[0].findAll("span")[0].text.strip()
                img = item.find_all("div", {"class": "alignleft"})[0].find_all("img", {"class": "product-images"})[0].get("data-src")

                try:
                    prix = int(item.find_all("span", {"class": "price"})[0].text.strip().replace(u'FCFA', '').replace(u'\xa0', ''))
                except:
                    prix=0



                produits.append(
                {
                'id': '',
                'libProduct': lib,
                'slug': '',
                'descProduct': '',
                'priceProduct': prix,
                'imgProduct': img,
                'numSeller': '',
                'src': site,
                'urlProduct': site + url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                })

            except:
                continue

    return produits

#print(scrapJumiaDeals(origin=1))

"""INSERTION DES PRODUITS"""

produits = scrapJumiaDeals(origin=1)
insertProduct(user='root',passW='',host='localhost',dbname='cameroun', produits=produits)
