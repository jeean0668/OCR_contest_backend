import NaverShopSearch

def isEnglishOrKorean(input_s): #한글인지 영어인지 판별
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return "k" if k_count>1 else "e"

texts = "DALEAF galactomyces better perfume shampoo 1000ml"

if isEnglishOrKorean(texts) == "k":
    text_search = texts
else:
    text_search = NaverShopSearch.hangul_sort(NaverShopSearch.get_translate(texts))[0]

print(text_search)
url = NaverShopSearch.Return_NaverUrl(text_search)
final_ingridient = NaverShopSearch.Make_Sentence(NaverShopSearch.ingridient(url))

print(final_ingridient)