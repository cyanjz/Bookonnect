import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "bookonnect.settings")

django.setup()

from books.models import *


def clean_book_description():
    books = Book.objects.all()
    for book in books:
        original_description = book.book_description
        processed_description = re.sub(r'&lt;', '', original_description)
        processed_description = re.sub(r'&gt;', '', processed_description)
        book.book_description = processed_description
        book.save()


if __name__ == '__main__':
    clean_book_description()