import os, io
os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'D:/Project/flutter_application_1/OCR_contest_backend/VisionAPI/eighth-parity-333905-9ec25f073c68.json'

from flask import Flask, request, flash, redirect, url_for, jsonify
from PIL import Image
from werkzeug.utils import secure_filename
import sys
import base64
import cv2

import NaverShopSearch

from VisionAPI import vision_api

UPLOAD_FOLDER = './upload'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods = ['POST'])
def upload():
    
    # POST로 front에서 이미지를 가져와 저장
    file = request.form.get('file')
    path = os.path.join('upload', 'sample.png')
    
    with open(path, 'wb') as fh:
        fh.write(base64.decodebytes(file.encode('utf-8')))
    
    texts = vision_api(path)
    try:
        data = NaverShopSearch.ingridient(NaverShopSearch.Return_NaverUrl(texts))
        sentence = NaverShopSearch.Make_Sentence(data)
    except:
        sentence = "네이버쇼핑에 성분이 나와있지 않습니다."
    print(sentence)
    data = {"filename" : 'sample.jpg', "texts" : texts}
    return jsonify(data)


if __name__ == "__main__":
    app.run(host = "211.244.91.156", port = 8000)
    #'https://211.244.91.156'
