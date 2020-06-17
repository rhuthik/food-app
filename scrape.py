from bs4 import BeautifulSoup 
import requests
with open('test.html') as html_file:
    soup =BeautifulSoup(html_file, 'lxml')

article = soup.find('article')
#print(article.prettify())
headline = article.h3.a.text
print(headline)