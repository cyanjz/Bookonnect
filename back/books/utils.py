from django.conf import settings
from requests import request
from pprint import pprint
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAi
import requests, json, os, sys
from pydantic import BaseModel
from PIL import Image
import json


# 1. load .env & initialize constants
load_dotenv()

API_KEYS = {
    'aladin': os.getenv('ALADIN_API_KEY'),
    'openai': os.getenv('OPENAI_API_KEY'),
}

API_URLS = {
    'aladinList': 'http://www.aladin.co.kr/ttb/api/ItemList.aspx',
}


API_KEY = API_KEYS['openai']
client = OpenAI(api_key=API_KEY)

# 2. fetch books from aladin api service
# cols
'''
# 일단 bestsellers만 parsing하여 db 저장, 결과 보기.

# Book table
book_title : title
book_description : description
author : 새로운 json 만들어야 할듯.
book_ISBN13 : isbn13
book_cover_img : cover
book_publisher : publisher
book_pu_date : pubDate
customer_review_rank : null
book_embedding : 생성 알고리즘 작성하기.


# Author table
author_pk : pk
author_name : (지은이) 정보 parsing
author_info : wikipedia에서 정보 가져오기.
author_profile_img : wikipedia에서 정보 가져오기.
author_info_mp3 : author_info있으면 만들기.
'''

# 알라딘 API 사용하여 도서 정보 가져오기.
class FetchBooks:
    def __init__(self):
        QueryTypes =  ['ItemNewAll', 'ItemNewSpecial', 'Bestseller', 'BlogBest']
    # fetch book list.
    # problem -> need to parse in different ways.
    @classmethod
    def aladinList(cls, QueryType='Bestseller'):
        # 1. request
        api_key = API_KEYS['aladin']
        api_url = API_URLS['aladinList']
        params = {
            'TTBKey': api_key,
            'QueryType': QueryType,
            'SearchTarget': 'Book',
            'Output': 'JS',
            'Version': 20131101,
        }
        resp = request(method='get', url=api_url, params=params)
        with open(f'./{QueryType}_data.json', 'w', encoding='utf-8') as fp:
            json.dump(resp.json(), fp, ensure_ascii=False, indent=4)

        # 2. parse data
        bookjson = []
        bestsellerjson = []
        authorjson = []
        for i, item in enumerate(resp.json().get('item')):
            # parse book info
            book_fields = {
                'title': item.title,
                'book_description': item.description,
                'book_ISBN13': item.isbn13,
                'book_cover_img': item.cover,
                'book_publisher': item.publisher,
                'book_pub_date': item.pubDate,
                'customer_review_rank': None,
                'book_embedding' : None,
            }
            book_item = {
                "model": "books.book",
                "pk": i + 1,
                "fields": book_fields,
            }
            bookjson.append(book_item)

            # parse bestseller info
            bestseller_fields = {
                'bestseller_book': i + 1,
                'bestseller_rank': item.bestRank,
            }
            bestseller_item = {
                "model": "books.bestseller",
                "pk": i + 1,
                "fields": bestseller_fields,
            }
            bestsellerjson.append(bestseller_item)

            # parse author info
            author_fields = {
                'bestseller_book': i + 1,
                'bestseller_rank': item.bestRank,
            }
            author_item = {
                "model": "books.bestseller",
                "pk": i + 1,
                "fields": bestseller_fields,
            }
            authorjson.append(author_item)



system_content = '''
당신은 구조화 되지 않은 데이터를 JSON 형식으로 변환하는 AI입니다.
사용자가 특정 작가에 대한 설명을 제공하면, 작가 정보와 대표 작품 목록을 JSON 형식으로 추출하세요.
json에 필요한 text이외의 text를 출력해서는 안됩니다.
답변은 항상 {로 시작해서 }로 끝나는 양식이어야 합니다.

아래는 답변의 예시입니다.
{
'masterpiece' : '데미안, 싯다르타, 나르치스와 골드문트, 유리말 유희, 보트',
'author_summary' : '헤르만 카를 헤세(독일어 : Hermann Karl Hesse, 1877년 7월 2일 ~ 1962년 8월 9일)는 독일계 스위스인이며, 시인, 소설가, 화가이다.'
}
'''
thread_context = '''
당신은 사용자의 도서 리뷰를 읽고 핵심 감정 5개를 추출해내는 ai 입니다.
추출된 감정 5개를 comma로 나눠서 반환해주세요.
감정 5개를 제외한 다른 정보를 응답해서는 안됩니다.
응답 예시 : '슬픔, 기쁨, 행복, 만족감, 허무함'
'''




class AuthorSummary(BaseModel):
    masterpiece : str
    author_summary : str


def get_ai_summary(context):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": context},
        ],
        response_format=AuthorSummary,
    )

    summary = completion.choices[0].message.content
    return summary


def get_author_info(kw):
    url = 'https://ko.wikipedia.org/w/api.php'
    params = {
        'action' : 'parse',
        'page' : kw,
        'format' : 'json',
    }
    fp = open('o.txt', 'w')
    # get request and load response to bs4
    resp = requests.get(url, params)
    try:
        data = resp.json()['parse']['text']['*']
    except:
        return False, False
    soup = BeautifulSoup(data, 'html.parser')
    
    # for ai summary
    content_div = soup.select_one('div.mw-content-ltr')
    content_text = ''
    for child in content_div.children:
        if '참조주' in child.text:
            break
        content_text += child.text
    # run ai summary
    result = get_ai_summary(content_text)
    author_info = json.loads(result)
    
    # cover image
    cover_image = soup.select_one('td.infobox-image > span > a > img')
    cover_image_url = cover_image.get('src')
    if cover_image_url.startswith("//"):
        cover_image_url = 'https:' + cover_image_url
    return cover_image_url, author_info


# generate thread image
def get_ai_thread_kw(context):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": thread_context},
            {"role": "user", "content": context},
        ],
    )

    summary = completion.choices[0].message.content
    return summary


def get_thread_image(prompt):
    feelings = get_ai_thread_kw(prompt)
    thread_cover_context = f'''
    당신은 감정 5개를 바탕으로 이미지를 그려주는 ai 입니다.
    창의적이고 감성적으로 표현해 주세요.
    아래의 콤마로 나눠진 감정 5개를 바탕으로 이미지를 생성해주세요.
    감정 또는 상황 : {feelings}
    '''
    response = client.images.generate(
        model="dall-e-3",
        prompt=thread_cover_context,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    img_url = response.data[0].url
    return img_url
