from django.conf import settings
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI
import requests, json, os
from pydantic import BaseModel
import json

# load .env & initialize constants
load_dotenv()
API_KEYS = {
    'aladin': os.getenv('ALADIN_API_KEY'),
    'openai': os.getenv('OPENAI_API_KEY'),
}

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
        client = OpenAI(api_key=API_KEYS['openai'])

    # 1. context를 기반으로 작가 정보 요약, 대표 작품 추출
    def get_ai_summary(self, context):
        completion = self.client.beta.chat.completions.parse(
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
            return '', ''
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
        completion = self.client.beta.chat.completions.parse(
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
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=thread_cover_context,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        img_url = response.data[0].url
        return img_url
