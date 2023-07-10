import requests
from bs4 import BeautifulSoup as BS
import csv
import time


def get_content(url):
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
        }
    resp = requests.get(url, headers=header)
    rows = []
    if resp.status_code == 200:
        page = BS(resp.text, 'html.parser')
        type_auto = page.find('h1')
        h1 = type_auto.text
        main_div = page.find('div', attrs={'class':'tile-list'})
        list_div = main_div.find_all('div', attrs={'class':'tile-item'})
        for it in list_div:
            topic = it.find('div', attrs={'class': 'sticker-product ru sticker-product-leader'})
            if topic is not None:
                description = it.find('div', attrs={'class': 'tile-title'})
                titles = description.a['title']
                href = 'https://detali.zp.ua' + description.a['href']
                tmp = {'model':h1, 'title': titles, 'href':href}
                print(tmp)
                rows.append(tmp)

    return rows


def get_page(url):
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
    rows =[]
    resp = requests.get(url, headers=header)
    if resp.status_code == 200:
        page = BS(resp.text, 'html.parser')
        list_pages = page.find('div', attrs={'class':'catalog-navigation'})
        if list_pages is None:
            rows = get_content(url)
        else:
            pages=list_pages.find_all('a', attrs = {'class':'float-left mr5'})
            rows = get_content(url)
            for pag in pages:
                href_= pag.get('href')
                print(href_)
                rows += get_content('https://detali.zp.ua'+href_)
                time.sleep(5)
    return rows


def get_cat():
    url = 'https://detali.zp.ua/catalog/10000163-Geely/'
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
    resp = requests.get(url, headers=header)
    rows =[]
    if resp.status_code == 200:
        page = BS(resp.text, 'html.parser')
        main_div = page.find('div', attrs={'class':'sub-cats-accordion'})
        final_div= main_div.find_all('div', attrs={'class':'sub-cats-item'})
        for item in final_div:
            href = 'https://detali.zp.ua' + item.a['href']
            rows += get_page(href)
            time.sleep(5)


    csv_title = ['model', 'title', 'href']
    with open('top_sale.csv', 'w') as f:
        wr = csv.DictWriter(f, fieldnames=csv_title, delimiter=';')
        wr.writeheader()
        wr.writerows(rows)


if __name__ == '__main__':
    get_cat()

