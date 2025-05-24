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


# III. Open AI
class OpenAiAPI:
    class AuthorSummary(BaseModel):
        masterpiece : str
        author_summary : str
    
    def __init__(self):
        # 0. AI prompting
        self.system_content = '''
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
        self.thread_context = '''
            당신은 사용자의 도서 리뷰를 읽고 핵심 감정 5개를 추출해내는 ai 입니다.
            추출된 감정 5개를 comma로 나눠서 반환해주세요.
            감정 5개를 제외한 다른 정보를 응답해서는 안됩니다.
            응답 예시 : '슬픔, 기쁨, 행복, 만족감, 허무함'
        '''

    # 1. context를 기반으로 작가 정보 요약, 대표 작품 추출
    def get_ai_summary(self, context):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_content},
                {"role": "user", "content": context},
            ],
            response_format= self.AuthorSummary,
        )
        summary = completion.choices[0].message.content
        return summary
    
    # 2. wikipedia API를 사용한 작가 정보 추출
    def get_author_info(self, kw):
        url = 'https://ko.wikipedia.org/w/api.php'
        # params = {
        #     'action' : 'query',
        #     'list': 'search',
        #     'srsearch' : f'intitle:{kw} (작가)',
        #     'format' : 'json',
        # }
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
        result = self.get_ai_summary(content_text)
        author_info = json.loads(result)
        
        # cover image
        cover_image = soup.select_one('td.infobox-image > span > a > img')
        try:
            cover_image_url = cover_image.get('src')
            if cover_image_url.startswith("//"):
                cover_image_url = 'https:' + cover_image_url
        except:
            cover_image_url = ''
            print('cover image not found!')
        return cover_image_url, author_info
    
    # 3. thread cover 생성을 위한 대표 감정 추출
    def get_ai_thread_kw(self, context):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.thread_context},
                {"role": "user", "content": context},
            ],
        )

        summary = completion.choices[0].message.content
        return summary

    # 4. thread image 생성.
    def get_thread_image(self, prompt):
        feelings = self.get_ai_thread_kw(prompt)
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


ai_instance = OpenAiAPI()
# print(ai_instance.get_author_info('한강 (작가)'))
# print(ai_instance.get_author_info('한강'))

fetchAladin()