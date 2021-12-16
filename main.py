import os, io
os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/COMG/programming/AI_Backend/eighth-parity-333905-9ec25f073c68.json'

from flask import Flask, request, flash, redirect, url_for, jsonify
from PIL import Image
from werkzeug.utils import secure_filename
import sys
import base64
import cv2

import NaverShopSearch

from VisionAPI import vision_api

import NaverShopSearch

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
    
    # debuging용
    #texts = 'while debugin...'
    #sentence = texts
    texts = vision_api(path)
    try:
        data = NaverShopSearch.ingridient(NaverShopSearch.Return_NaverUrl(texts))
        sentence = NaverShopSearch.Make_Sentence(data)
    except:
        sentence = "네이버쇼핑에 성분이 나와있지 않습니다."
    print(sentence)
    data = {
        "filename" : 'sample.jpg', 
        "texts" : texts, 
        "ingredients" : sentence
    }
    return jsonify(data)


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
    app.run(host = "180.64.184.81", port = 8000)
    #'https://211.244.91.156'
