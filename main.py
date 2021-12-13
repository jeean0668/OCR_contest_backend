import easyocr
from flask import Flask, request, flash, redirect, url_for, jsonify
from PIL import Image
from werkzeug.utils import secure_filename
import os
import sys
import base64

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import quote_plus
from webdriver_manager.chrome import ChromeDriverManager

import NaverShopSearch

UPLOAD_FOLDER = './upload'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods = ['GET'])
def init():
    return 'hello world'

@app.route('/upload', methods = ['POST'])
def upload():
    
    # POST로 front에서 이미지를 가져와 저장
    file = request.form.get('file')
    path = os.path.join('upload', 'sample.png')
    with open(path, 'wb') as fh:
        fh.write(base64.decodebytes(file.encode('utf-8')))
    # 저장된 이미지를 easyocr에 넣고 판독
    reader = easyocr.Reader(['ko', 'en'])
    result = reader.readtext(path)
    # 정확도가 0.5 이상인 text들만 저장
    texts = []
    for r in result:
        if r[2] >= 0.5:
            texts.append(r[1])
    
    text = " ".join(texts)
    print(text)
    if isEnglishOrKorean(text) == "k":
        texts = NaverShopSearch.hangul_sort(text)[0]
        text_search = texts
    else:
        texts = Google_Search(text)
        text_search = NaverShopSearch.hangul_sort(NaverShopSearch.get_translate(texts))[0]
    try:
        url = NaverShopSearch.Return_NaverUrl(text_search)
        final_ingridient = NaverShopSearch.Make_Sentence(NaverShopSearch.ingridient(url))
    except:
        print("There're no items")
    data = {"filename" : 'sample.jpg', "texts" : texts}
    return jsonify(data)


def Google_Search(Text):
  url = 'https://www.google.com/search?q='
  kword = Text
  base_url = url + quote_plus(kword)

  chrome_options = webdriver.ChromeOptions()
  #chrome_options.headless = True
  #chrome_options.add_argument('--no-sandbox')
  #chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.get(base_url)

  html = driver.page_source
  soup = BeautifulSoup(html,"lxml")

  v = soup.select('.yuRUbf')
  result = v[0].select_one('.LC20lb.DKV0Md').text
  link = v[0].a.attrs['href']

  driver.close()                       # 크롬 창 닫기
  return result

def isEnglishOrKorean(input_s): #한글인지 영어인지 판별
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return "k" if k_count>1 else "e"

if __name__ == "__main__":
    app.run(host = "211.244.91.156", port = 8000)
    #'https://211.244.91.156'
