import os, io, re

from google.cloud import vision
from google.cloud import vision_v1


def vision_api(path):
    client = vision.ImageAnnotatorClient()
    #path_dir = os.path.join(os.path.dirname(__file__),'txt')
    #removeAllFile(path_dir)

    # Loads the image into memory
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    with open('./txt/'+'result.txt', "w",encoding='UTF-8') as f:
        f.write(texts[0].description)
    
    textlist = ''
    for text in texts:
        textlist = textlist + text.description

    keyword = ["샴푸","트리트먼트","세럼","토너","크림","에센스","앰플","패드","프라이머","바디워시","염색","토닉","부스터","쿠션"]
    keyword2 = ["전성분","사용시의","효능효과","사용 시의","비매품"]
    try:
        idx2 = []
        for i in keyword2:
            if textlist.find(i)>0:
                idx2.append(textlist.find(i))
        ingredient = textlist[smallest_number12(idx2)[0]:smallest_number12(idx2)[1]+1]
        ingredients = remove(ingredient)
    except:
        ingredients = "전성분이 나와있지 않습니다."
    f = open(os.path.join(os.path.dirname(__file__),'txt',"result.txt"),encoding='UTF-8')
    lines = []
    sen = []
    for paragraph in f:
        lines = str.split(paragraph,"\n")
        for each_line in lines:
            for i in keyword:
                if each_line.find(i)>0:
                    sen.append(each_line)
    final = []
    for text in sen:
        if len(text) <= 40:
            final.append(text)
    final_text = ""
    flag=0
    if len(final) != 0:
        for i in final:
            if "제품명" in i:
                blnk = i.rfind("]")
                final_text += i[blnk+2:]
                flag = 1
            
        if flag == 0:
            final_text += final[0]
    else:
        final_text = "제품명이 나와있지 않습니다."
    
    return final_text, ingredients

def smallest_number12(arr):
    unique_nums = set(arr)
    sorted_nums = sorted(unique_nums, reverse=False)
    return sorted_nums[0], sorted_nums[1]

def remove(arr):
    result = arr.replace("[","")[0:-1]
    result = arr.replace("]","")[0:-1]
    result = arr.replace("\n","")[0:-1]
    return result
