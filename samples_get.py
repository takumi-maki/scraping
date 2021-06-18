import chromedriver_binary
from selenium import webdriver
from PIL import Image
import io
from urllib import request

driver = webdriver.Chrome()

word = 'マッチョ'
driver.get('https://search.yahoo.co.jp/image/search?p={}&aq=-1&ai=025b24b8-536d-4ce3-ab93-82b4e2e0551d&ts=4028&sfp=1&ei=UTF-8&fr=sfp_as'.format(word))

# １ページ分の画像を入手
elems = driver.find_elements_by_class_name('sw-Thumbnail')
for index, elem in enumerate(elems):
    elem = elem.find_element_by_tag_name('img')
    url = elem.get_attribute('src')

    f = io.BytesIO(request.urlopen(url).read())
    img = Image.open(f)
    img.save('image/jk/img{}.jpg'.format(index))


driver.close()
