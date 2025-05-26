from pprint import pprint
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
import re
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "bookonnect.settings")

import django
django.setup()

from books.models import *

# 전역 변수

with open('01_books_raw.json', 'r', encoding='utf-8') as fp:
    data = json.load(fp)

with open('categories.json', 'r', encoding='utf-8') as fp:
    category_list = json.load(fp)
    # {pk, name, cid_list}
for category_element in category_list:
    category_instance = Category(
        category_name = category_element['name']
    )
    category_instance.save()

sale_point_list = [(i, elem['item'][0]['salesPoint']) for i, elem in enumerate(data)]
sale_point_sorted = sorted(sale_point_list, key=lambda x: x[1])
rank_mapper = {}
rank = 0
for idx, point in sale_point_sorted:
    rank_mapper[idx] = rank+1
    rank += 1

ai_instane = OpenAiAPI()


# 함수
'''
authorinfo 위치
subInfo -> authors -> authorName, authorInfo, authorPhoto
author_name : authorName,
author_info : authorInfo,
author_profile_img : authorPhoto
author_info_mp3 : authorInfo 사용해서 mp3 만들기.
# author_masterpeice -> wikipedia 사용. -> 쓰지 말죠 걍
'''
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
        try:
            tts = gTTS(text=author_info['author_summary'], lang='ko')
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            try:
                author.author_info_mp3.save(f"{author_name}_audio.mp3", ContentFile(mp3_fp.read()))
            except:
                print('mp3 저장 실패...')
            author.author_info=author_info['author_summary']
        except Exception as e:
            print('gtts 생성 실패...')
            print(author_info)
            print(e)
    author.save()
    return author

def parse_author_info(elem):
    original_author = elem['author']
    match = re.search(r'^(.*?)\(', original_author)
    if match:
        author_name = match.group(1).strip()
    else:
        author_name = original_author
    try:
        for temp in elem['subInfo']['authors']:
            if temp['authorName'] == author_name:
                author_info_dict = temp
        if Author.objects.filter(author_name=author_info_dict['authorName']).exists():
            return Author.objects.get(author_name=author_info_dict['authorName'])
        author_info = author_info_dict.get('authorInfo', '')
        author_photo_url = author_info_dict.get('authorPhoto', '')
    except Exception as e:
        author_info = ''
        author_photo_url = ''
        print('can not find value')
    
    if author_info == '' or author_photo_url == '':
        author_wiki_img_url, author_wiki_info = ai_instane.get_author_info(f'{author_name} (작가)')
        if author_wiki_img_url == '':
            author_wiki_img_url, author_wiki_info = ai_instane.get_author_info(author_name)
        author_info = author_info if author_info else author_wiki_info
        author_photo_url = author_photo_url if author_photo_url else author_wiki_img_url
    author_info_temp = {
        'author_summary' : author_info
    }
    author = save_author(author_photo_url, author_info_temp, author_name)
    return author


'''
book_title : title
book_description : description
book_ISBN13 : isbn13
book_cover_img : cover
book_publisher : publisher
book_pub_date : pubDate
book_ranking : salesPoint기반으로 만들기
book_author_id :  -> 적절한 로직으로 만들고 연결.
category_id : -> 적절한 로직으로 만들고 연결
book_embedding : 아직 안만듦.
book_customer_review_rank : customerReviewRank
'''

def parse_book_info(elem, author_name, best_rank, index):
    # parse book info
    cid = elem['categoryId']
    for idx, category_element in enumerate(category_list):
        if cid in category_element['cid']:
            category_instance = Category.objects.get(pk=idx+1)
    cleaned_first = re.sub(r'&lt', '', elem['description'])
    cleaned_second = re.sub(r'&gt', '', cleaned_first)
    try:
        if Book.objects.filter(book_ISBN13=elem['isbn13']).exists():
            return
        if desc_dict[index] == None:
            book = Book(
                category=category_instance,
                author=Author.objects.get(author_name=author_name),
                book_title=elem['title'],
                book_description=cleaned_second,
                book_ISBN13=elem['isbn13'],
                book_publisher=elem['publisher'],
                book_pub_date=elem['pubDate'],
                book_salesPoint=elem['salesPoint'],
                book_customer_review_rank=None,
                book_embedding=None,
            )
        else:
            book = Book(
                category=category_instance,
                author=Author.objects.get(author_name=author_name),
                book_title=elem['title'],
                book_description=cleaned_second,
                book_ISBN13=elem['isbn13'],
                book_publisher=elem['publisher'],
                book_pub_date=elem['pubDate'],
                book_salesPoint=elem['salesPoint'],
                book_customer_review_rank=None,
                book_embedding=embeddings[desc_dict[index]],
            )
        book_cover_img_url = elem['cover']
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
    except:
        print('도서 정보 가져오기에 실패했습니다.')


def get_embedding():
    description_list = []
    description_dict = {}
    top = -1
    for i, elem in enumerate(data):
        # description이 존재하는 경우
        if elem['item'][0]['description']:
            top += 1
            description_list.append(elem['item'][0]['description'])
            description_dict[i] = top
        else:
            description_dict[i] = None
        # if i == 3:
        #     break
    result = ai_instane.get_description_embedding(description_list)
    result = [item.embedding for item in result]
    return result, description_list, description_dict


embeddings, desc_list, desc_dict = get_embedding()


for i, temp in enumerate(data):
    elem = temp['item'][0]
    # 1. author 정보
    author = parse_author_info(elem)

    # 2. 도서 정보
    parse_book_info(elem, author.author_name, rank_mapper[i], i)
    # if i == 3:
    #     break
