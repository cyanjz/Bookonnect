from ..utils import OpenAiAPI
import json

ai_instance = OpenAiAPI()
with open('books.json', 'r', encoding='utf-8') as fp:
    data = json.load(fp)