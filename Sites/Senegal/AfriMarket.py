from bs4 import BeautifulSoup
import requests


def categoryAfriMarket():
    site = 'https://afrimarket.sn/'
    page_response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
    page_content = BeautifulSoup(page_response.content, "html.parser")

    category = page_content.find('ul',{"class":"ms-topmenu"}).findAll("li",{"class":"topm"})

    categories_urls = []

    for item in category:
        urlCategory = item.find('a',{"class":"ms-label"}).get("href")

        categories_urls.append(
            urlCategory
        )

    return categories_urls[2:-1]

#print(categoryAfriMarket())


def subCategoryAfriMarket():

    categories_urls = categoryAfriMarket()
    subUrl = []

    for el in categories_urls:
        page_response = requests.get(el, headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        subCategories = page_content.find('div', {"class": "filter-options-content categoryFilterDesktop"}).findAll('li',{"class":"item"})


        for item in subCategories:
            name = item.findAll('a')[0].text.split(' ')
            subCategoryName = name[0:-1]
            s= " "
            subCategoryUrl = item.findAll('a')[0].get("href")

            subUrl.append({
                'url':subCategoryUrl,
                'name': s.join(subCategoryName).replace('\n','')
            })

    return subUrl

#print(subCategoryAfriMarket())


def getAllPage():

    subUrl = subCategoryAfriMarket()
    page = []


    for url in subUrl:
        page_response = requests.get(url['url'], headers={'User-Agent': 'Mozilla/5.0'})
        page_content = BeautifulSoup(page_response.content, "html.parser")

        try:
            sup = page_content.find('div', {"class": "pages"}).findAll('li', {"class": "item"})[-2].find('span',{"class":"label"}).text
            maxPage = int(page_content.find('div', {"class": "pages"}).findAll('li', {"class": "item"})[-2].text.replace(sup,'')) + 1
            id = list(range(maxPage))
            del id[0]

            for el in id:
                link = url['url'] + "?p=" + str(el)

                page.append({
                    'url':link,
                    'name':url['name']
                })
        except:

            link1 = url['url']

            page.append({
                'url':link1,
                'name':url['name']
            })

    return page

#print(getAllPage())

def scrapAfriMarket(origin):

    site = 'https://afrimarket.sn/'
    page = getAllPage()
    produits = []

    for link in page:
        try:
            page_response = requests.get(link["url"], headers={'User-Agent': 'Mozilla/5.0'})
            page_content = BeautifulSoup(page_response.content, "html.parser")

            logo = "http://137.74.199.121/img/logo/sn/afrimArket.jpg"
            logoS = "http://137.74.199.121/img/logo/sn/logoS/afrimarket.jpg"
            annonce = page_content.findAll("li", {"class": "item"})
        except:
            continue


        for item in annonce:
            try:
                url = item.find("div", {"class": "product-item-info"}).findAll('a', {"class": "product-item-link"})[0].get("href")
                lib = item.find("div", {"class": "product-item-info"}).findAll('a', {"class": "product-item-link"})[0].text.replace('\n','')
                img = item.findAll("img")[0].get("src")
                try:
                    prix = int(item.findAll("span", {"class": "price"})[0].text.replace(u'\xa0', '').replace(u'FCFA', ''))
                except:
                    prix=0

                produits.append(
                {
                'libProduct': lib,
                'slug': '',
                'descProduct': '',
                'priceProduct': prix,
                'imgProduct': img,
                'numSeller': '',
                'src': site,
                'urlProduct': url,
                'logo': logo,
                'logoS':logoS,
                'origin': origin,
                "country": "sn",
                "subcategory":link['name']
                }
                )

            except:
                continue

    return produits

#print(scrapAfriMarket(origin=0))

"""INSERTION DES PRODUITS"""

produits = scrapAfriMarket(origin=0)
url = 'https://sn.comparez.co/api/v1/ads/legacy/'
for item in produits:
    try:
        response = requests.post(url, data=item)
        # api response
        print(response.json())
    except:
        pass


