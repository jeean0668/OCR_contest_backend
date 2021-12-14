import os, io, re
os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'D:/Project/flutter_application_1/OCR_contest_backend/VisionAPI/eighth-parity-333905-9ec25f073c68.json'

from VisionAPI import vision_api
import NaverShopSearch

path = os.path.join(os.path.dirname(__file__),'resources')
file_list = os.listdir(path)

path = os.path.join(path,file_list[2])
texts = vision_api(path)
try:
    data = NaverShopSearch.ingridient(NaverShopSearch.Return_NaverUrl(texts))
    sentence = NaverShopSearch.Make_Sentence(data)
except:
    sentence = "네이버쇼핑에 성분이 나와있지 않습니다."

print(texts, sentence)