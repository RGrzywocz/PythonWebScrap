import bs4
import requests
import pandas as pd
import openpyxl

pages = []
prices = []
stars = []
titles = []
urls = []
pagesToScrape = int(input('Ile stron?'))

pageUrl = 'http://books.toscrape.com/'

for i in range(1, pagesToScrape + 1):
    url = ('http://books.toscrape.com/catalogue/page-{}.html').format(i)
    pages.append(url)
for item in pages:
    page = requests.get(item)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    for i in soup.find_all('h3'):
        titles.append(i.getText())
    for i in soup.find_all('p', class_= 'price_color'):
        prices.append(i.getText().replace('Â£', '$'))
    for i in soup.find_all('p', class_= 'star-rating'):
        for k, v in i.attrs.items():
            star = v[1]
            stars.append(star)
    for i in soup.find_all('img', class_= 'thumbnail'):
        for k,v in i.attrs.items():

            toappend = ('http://books.toscrape.com/' + i['src']).replace('../', '')
            if toappend not in urls:
                urls.append(toappend)


data = {'Title': titles, 'Prices': prices, 'Stars': stars, 'Url': urls}
print(len(titles), len(prices), len(stars), len(urls))
df = pd.DataFrame(data=data)
df.index += 1
df.to_excel('test.xlsx')
