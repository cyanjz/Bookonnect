from books.utils import OpenAiAPI
from django.conf import settings
from requests import request
from pprint import pprint
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI
import requests, json, os
from io import BytesIO
from pydantic import BaseModel
from PIL import Image
from gtts import gTTS
import json
from django.core.files.base import ContentFile
from random import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "bookonnect.settings")

import django
django.setup()

from books.models import *


# load .env & initialize constants
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

# I. 카테고리 정보 불러오기.
with open('categories.json', 'r', encoding='utf-8') as fp:
    category_list = json.load(fp)
    # {pk, name, cid_list}
for category_element in category_list:
    category_instance = Category(
        category_name = category_element['name']
    )
    category_instance.save()

# II. 도서 정보 가져오기.
def fetchAladin(QueryType='Bestseller'):
    # 1. request
    api_key = API_KEYS['aladin']
    api_url = API_URLS['aladinList']
    params = {
        'TTBKey': api_key,
        'QueryType': QueryType,
        'SearchTarget': 'Book',
        'Output': 'JS',
        'Version': 20131101,
        'MaxResults': 50,
    }
    resp = request(method='get', url=api_url, params=params)
    with open(f'./{QueryType}_data.json', 'w', encoding='utf-8') as fp:
        json.dump(resp.json(), fp, ensure_ascii=False, indent=4)

    # 2. parse data
    ai_instance = OpenAiAPI()
    for i, item in enumerate(resp.json().get('item')):
        # parse author info
        # check the author already exists or not
        author_name = item['author'].split("(지은이)")[0].rstrip()
        if Author.objects.filter(author_name=author_name).exists():
            pass
        else:
            author_image_url, author_wiki_info = ai_instance.get_author_info(f'{author_name} (작가)')
            if author_image_url == False:
                author_image_url, author_wiki_info = ai_instance.get_author_info(author_name)
            
            save_author(author_image_url, author_wiki_info, author_name)
        
        # parse book info
        cid = item['categoryId']
        for idx, category_element in enumerate(category_list):
            if cid in category_element['cid']:
                category_instance = Category.objects.get(pk=idx+1)
        book = Book(
            category=category_instance,
            author=Author.objects.get(author_name=author_name),
            book_title=item['title'],
            book_description=item['description'],
            book_ISBN13=item['isbn13'],
            book_publisher=item['publisher'],
            book_pub_date=item['pubDate'],
            book_customer_review_rank=None,
            book_embedding= None,
            book_ranking= item['bestRank'],
        )
        book_cover_img_url = item['cover']
        if book_cover_img_url:
            try:
                buffer = BytesIO()
                response = requests.get(book_cover_img_url, stream=True)
                image = Image.open(response.raw)
                image.save(buffer, format='png')
                image_bytes = buffer.getvalue()
                book.book_cover_img.save(f"{book.book_title[:10]}_cover.jpg", ContentFile(image_bytes))
            except Exception as e:
                print(f'도서 커버를 저장하는데 실패했습니다. - {e}')
        book.save()


def save_author(img_url, author_info, author_name):
    author = Author(
        author_name=author_name,
    )
    # image
    if img_url:
        try:
            buffer = BytesIO()
            response = requests.get(img_url, stream=True)
            image = Image.open(response.raw)
            image.save(buffer, format='png')
            image_bytes = buffer.getvalue()
            author.author_profile_img.save(f"{author_name}_profile.jpg", ContentFile(image_bytes))
        except Exception as e:
            print(f'프로필 저장 실패... : {str(e)}')

    # gtts
    if author_info:
        if author_info['author_summary']:
            tts = gTTS(text=author_info['author_summary'], lang='ko')
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            try:
                author.author_info_mp3.save(f"{author_name}_audio.mp3", ContentFile(mp3_fp.read()))
            except:
                print('mp3 저장 실패...')
        author.author_info=author_info['author_summary']
        author.author_masterpeice=author_info['masterpiece'],
    author.save()
    return True


# II. update db
def update_embedding():
    books = Book.objects.all()
    ai_instance = OpenAiAPI()
    for book in books:
        # embedding update
        description = book.book_description
        if description == '':
            pass
        else:
            result = ai_instance.get_description_embedding([description])
            result = [item.embedding for item in result]
            book.book_embedding = result[0]
            book.save()

def update_recommended():
    books = Book.objects.all()
    for i, book in enumerate(books):
        if i % 5 == 0:
            book.book_recommened = True
            book.save()

update_embedding()
# update_recommended()

# fetchAladin()