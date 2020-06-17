from bs4 import BeautifulSoup 
import requests
url = 'https://www.bbcgoodfood.com/recipes/collection/easy'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
source = requests.get('https://www.bbcgoodfood.com/recipes/collection/easy').text
soup = BeautifulSoup(source,'lxml')
print(soup.prettify())