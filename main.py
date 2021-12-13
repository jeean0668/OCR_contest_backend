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
    reader = easyocr.Reader(['en', 'ko'])
    result = reader.readtext(path)
    # 정확도가 0.5 이상인 text들만 저장
    texts = []
    for r in result:
        if r[2] >= 0.5:
            texts.append(r[1])
    
    text = " ".join(texts)
    print(text)
    texts = Google_Search(text)
    print('ok2')
    print(texts)
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

if __name__ == "__main__":
    app.run(host = "180.64.184.81", port = 8000)
    #'https://211.244.91.156'
