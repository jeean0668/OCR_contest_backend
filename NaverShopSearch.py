import re
import requests
import urllib
import json
from bs4 import BeautifulSoup

def Return_NaverUrl(text):
    client_id = "okADh5t8E8j9Tmg_NEdc" # <-- client_id 기입
    client_secret = "n3HlKEzx4u" # <-- client_secret 기입

    query = text
    query = urllib.parse.quote(query)

    display = "1"

    url = "https://openapi.naver.com/v1/search/shop?query=" + query + "&display=" + display

    request = urllib.request.Request(url)
    request.add_header('X-Naver-Client-Id', client_id)
    request.add_header('X-Naver-Client-Secret', client_secret)

    response = urllib.request.urlopen(request)
    json_data = response.read().decode('utf-8')

    jsonObject = json.loads(json_data)
    jsonArray = jsonObject.get("items")

    url = "https://search.shopping.naver.com/catalog/" + jsonArray[0]['productId']
    print(url)
    return url

def ingridient(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        number = soup.select_one("#section_ingredient > div.analysisIngredient_analysis_list__1z2MW > h4 > em")
        Title = []
        Sub_Title = []

        skin = ["지성","건성","민감성"]
        Good = {"지성":"","건성":"","민감성":""}
        Bad = {"지성":"","건성":"","민감성":""}
        for i in range(int(number.get_text())):
                Title.append(soup.select_one('#section_ingredient > div.analysisIngredient_analysis_list__1z2MW > ul > li:nth-child('+str(i+1)+') > div.analysisIngredient_info__2mt8l > div').get_text())
                Sub_Title.append(soup.select_one('#section_ingredient > div.analysisIngredient_analysis_list__1z2MW > ul > li:nth-child('+str(i+1)+') > div.analysisIngredient_info__2mt8l > p').get_text())
            
        for i,v in enumerate(skin):
            Good[v] = soup.select_one('#section_ingredient > div.cosmeticIngredient_ingredient_info__1sTIL > div:nth-child(3) > div > div:nth-child('+str(i+1)+') > div > span.cosmeticIngredient_good__ds1UI').get_text()
            Bad[v]= soup.select_one('#section_ingredient > div.cosmeticIngredient_ingredient_info__1sTIL > div:nth-child(3) > div > div:nth-child('+str(i+1)+') > div > span.cosmeticIngredient_bad__2SrMG').get_text()
            
        return Title, Sub_Title, Good, Bad
    else : 
        print(response.status_code)


def Make_Sentence(data):

    title = data[0]
    sub_title = data[1]
    good = data[2]
    bad = data[3]

    final = []
    sentence = "분석성분으로 " + str(len(title)) + "가지가 있으며,"
    final.append(sentence)
    
    for key, value in good.items():
        if value !='0':
            sentence = key + "피부에 좋은 성분으로 " + value + "가지가 있습니다."
            final.append(sentence)

    for key, value in bad.items():
        if value !='0':
            sentence = key + "피부에 유해한 성분으로 " + value + "가지가 있습니다."
            final.append(sentence)
    
    count = 1
    for i,j in zip(title,sub_title):
        sentence = str(count) + "번 성분으로 " + i +"가 있으며 " + j +"로 사용됩니다."
        final.append(sentence)
        count+=1

    final_sentence = " ".join(final)

    return final_sentence
