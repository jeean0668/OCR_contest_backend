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
    
    print(texts)    
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
        ingredients = sort(ingredients)
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

def sort(ingredients):
    Good = {"지성 피부" : ["글리콜린산","살리실산","난 옥시놀-9,녹차","위치 하젤","레몬","캄파","멘톨클로로필","알라토인","티트리","감초","징크 옥사이트","칼렌 듈라 추출물","설퍼","트리클로잔","티타늄 옥사이드"], \
        "건성 피부" : ["히아루론산","글리세린","프로필렌 글라이콜","1,3-부틸렌 글라이콘","소디움PCA","비타민E","비타민A","비타민C","콜레젠","엘라스틴","아보카도 오일","이브닝 프라임 로즈 오일","오트밀 단백질",\
        "콩 추출물","카모마일","오이","복숭아","해조 추출물","상백피 추출물","코직산","알부틴","포토씨 추출물","베타카로틴","시어버터","파일워트 추출물","비타민B 복합체","판테놀"],\
        "민감성 피부" : ["비타민K","비타민F","호스트체스트넛 추출물","카모마일","알로에","콘플라워","알란토인","해조 추출물","티타늄 옥사이트"]}
    Bad = {"지성 피부" : ["트리글리세라이드","팔마티산염","미리스틴산","스테아르산염","스테아린산","코코넛오일","시어버터","바세린","옥시벤존","메톡시시나메이트"],\
       "건성 피부" : ["알코올","진흙","계면활성제","멘톨","페파민트"],"민감성 피부" : ["알코올","계면활성제","멘톨","페퍼민트","유칼립투스","아로마오일","고농도 과일산(AHA,BHA) 오렌지","딸기","레몬","레티놀","옥시벤존","메톡시 시나메이트",\
       "그 밖에 자신의 피부에 맞지않는 알레르기 물질 등"]}

    ingredients = ingredients.split()
    result = ""
    for key, value in Good.items():
        result = result + " " + key + "에 좋은 성분이"
        c=0
        for i in value:
            if i in ingredients:
                result = result + " " + i
                c+=1
        if c>0:
            result += "이 있습니다."
        else:
            result += " 없습니다."
    
    
    for key, value in Bad.items():
        result = result + " " + key + "에 유해한 성분이"
        c = 0
        for i in value:
            if i in ingredients:
                result = result + " " + i
                c+=1
        
        if c>0:
            result += "이 있습니다."
        else:
            result += " 없습니다."

    return result
