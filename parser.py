import requests
from bs4 import BeautifulSoup
import csv
import os

URL ='https://rozetka.com.ua/ua/notebooks/c80004/preset=game/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666',
    'accept':'*/*'
}
FILE = 'laptops.csv'

def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('li', class_='pagination__item')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='catalog-grid__cell')
    #print(items)
    laptops = []
    for item in items:
        try:
            price_old = item.find('div', class_='goods-tile__price--old price--gray ng-star-inserted').get_text().replace('\xa0', ' ')
            price_old_ = price_old[:-1]
            laptops.append({
                    'title': item.find('a', class_='goods-tile__heading').get_text(strip=True),
                    'link': item.find('a', class_='goods-tile__picture').get('href'),
                    'expired price': price_old_,
                    'price': item.find('span', class_='goods-tile__price-value').get_text().replace('\xa0', ' '),
                    'stars': item.find('div', class_='goods-tile__stars').find_next('svg').get('aria-label'),
                    'availability': item.find('div', class_='goods-tile__availability').get_text(strip=True)
            })
        except AttributeError:
            laptops.append({
                'title': item.find('a', class_='goods-tile__heading').get_text(strip=True),
                'link': item.find('a', class_='goods-tile__picture').get('href'),
                'expired price': 'There is no old price',
                'price': 'There is no price',
                'stars': 'There is no rating',
                'availability': item.find('div', class_='goods-tile__availability').get_text(strip=True)
            })
    #print(laptops)
    return laptops


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title', 'URL', 'Expired price', 'Price now', 'Rating', 'Condition'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['expired price'], item['price'], item['stars'], item['availability']])



def parse():
    html = get_html(URL)
    if html.status_code == 200:
        #get_content(html.text)
        laptops = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count+1):
            print(f'Scraping the page {page}/{pages_count} ...')
            url = f'https://rozetka.com.ua/ua/notebooks/c80004/page={page};seller=other/'
            html = get_html(url)
            laptops.extend(get_content(html.text))
        #print(laptops)
        save_file(laptops, FILE)
        #print(len(laptops))
        os.startfile(FILE)
    else:
        print("Error")

if __name__ == "__main__":
    parse()