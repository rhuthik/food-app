import requests
import lxml.html

html = requests.get("https://www.bbcgoodfood.com/recipes/collection/easy")
doc = lxml.html.fromstring(html.content)