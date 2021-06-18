import os
import chromedriver_binary
from selenium import webdriver
from PIL import Image
import io
from urllib import request

import time

driver = webdriver.Chrome()

# yahoo ログイン
driver.get('https://login.yahoo.co.jp/')
elem_username = driver.find_element_by_id('username')
elem_username.send_keys('uonomesyoukougun')
elem_next_btn = driver.find_element_by_id('btnNext')
elem_next_btn.click()
time.sleep(2)
elem_password = driver.find_element_by_id('passwd')
elem_password.send_keys('takumi')
elem_submit_btn = driver.find_element_by_id('btnSubmit')
elem_submit_btn.click()


word = "pizza"
save_dir = 'image/search'

# 保存するフォルダがなければ作る
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# yahooの画像へのアクセス
url = "https://search.yahoo.co.jp/image/search?p={}"
driver.get(url.format(word))

page = 0
# 4ページ分スクロール
while True:
    if page > 3:
        break
    prev_html = driver.page_source  # スクロール前のソースコード
    driver.execute_script(
        'window.scrollTo(0, document.body.scrollHeight);')  # 最下部までスクロール
    time.sleep(1.0)  # 1.0秒待機
    current_html = driver.page_source  # スクロール後のソースコード

    # スクロールの前後で変化がなければループを抜ける
    if prev_html != current_html:
        prev_html = current_html
        page += 1
    else:
        try:
            button = driver.find_element_by_class_name('sw-Button')
            button.click()
        except:
            break

#　画像タグを全て取得
elems = driver.find_elements_by_class_name('sw-Thumbnail')

for index, elem in enumerate(elems):
    elem = elem.find_element_by_tag_name('img')
    url = elem.get_attribute('src')

    f = io.BytesIO(request.urlopen(url).read())
    img = Image.open(f)
    img.save(save_dir + '/img{}.jpg'.format(index))

driver.close()
