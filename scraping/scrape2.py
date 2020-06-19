from bs4 import BeautifulSoup 
import requests
import csv
url = 'https://www.bbcgoodfood.com/recipes/collection/easy'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
source = requests.get('https://www.bbcgoodfood.com/recipes/collection/easy',headers = headers).text
soup = BeautifulSoup(source,'lxml')
#print(soup.prettify())
csv_file = open('bbc_scrape.csv','w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name','ingredient','method','image'])

for article in soup.find_all('article'):
    src = article.h3.a['href']
    link = f'https://www.bbcgoodfood.com{src}'
    #with open('links.json','w') as l:
        #json.dump(link,l)
    #print(link)
    foodsource = requests.get(link,headers = headers).text
    unique = BeautifulSoup(foodsource,'lxml')
    #print(unique.prettify())
    name = unique.find(class_='recipe-header__title').text
    #print(name)
    method = unique.find('div', class_='method').text
    #print(method)
    for check in unique.find_all(class_='ingredients-list__item'):
        ingred = check['content']
        ient = check.text
        #print(ingred)
    #ingred = unique.find_all(class_='ingredients-list__item')['content']
    image = unique.find(itemprop='image')['src']
    #print(image)
    csv_writer.writerow([name,ingred,method,image])

csv_file.close()


