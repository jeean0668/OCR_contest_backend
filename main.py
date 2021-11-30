import easyocr
from flask import Flask, request, flash, redirect, url_for, jsonify
from PIL import Image
from werkzeug.utils import secure_filename
import os
import sys
import base64

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
    #result = reader.readtext(path)
    
    
    # 정확도가 0.5 이상인 text들만 저장
    texts = []
    for r in result:
        if r[2] >= 0.5:
            texts.append(r[1])
    data = {"filename" : 'sample.jpg', "texts" : texts}
    return jsonify(data)

if __name__ == "__main__":
    app.run(host = "211.244.91.156", port = 8000)
    #'https://211.244.91.156'