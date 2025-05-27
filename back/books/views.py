from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Q, Case, When, IntegerField
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status, generics
from .serializers import (BookListSerializer, 
                          BookDetailSerializer, 
                          ThreadListSerializer, 
                          ThreadCreateSerializer, 
                          ThreadDetailSerializer, 
                          CommentListSerializer, 
                          CommentCreateSerializer, 
                          CommentUpdateSerializer,
                          ThreadUpdateSerializer,
                          CategoryListSerializer,
                          BookSearchSerializer)
from .models import (Book, Thread, Comment, Category)
from .utils import OpenAiAPI
from io import BytesIO
import requests
from PIL import Image
from django.core.files.base import ContentFile
import json
import numpy as np

ai_instance = OpenAiAPI()

def get_similarity(book_vector, user_vector):
    # book_vector, user_vector must be normalized before the function is called
    if book_vector is None:
        return 0
    else:
        book_vector = np.array(json.loads(book_vector))
        dot_product = np.dot(book_vector, user_vector)
        return dot_product


@api_view(['GET'])
def book_search_list(request):
    query = request.GET.get('q')
    books = Book.objects.filter(
        Q(book_description__icontains=query) | Q(book_title__icontains=query)
        )
    serializer = BookSearchSerializer(books, many=True)
    return Response(serializer.data)

# Create your views here.
# book views
@api_view(['GET'])
def book_list_create(request):
    if request.method == 'GET':
        query = request.GET.get('q', None)
        if query == None:
            books = get_list_or_404(Book)
        elif query == 'bestsellers':
            books = Book.objects.filter(book_ranking__lte=10).order_by('book_ranking')
        elif query == 'category':
            category_pk = int(request.GET.get('cId', None))
            category = get_object_or_404(Category, pk=category_pk)
            books = Book.objects.filter(category=category)
        elif query == 'recommended':
            books = Book.objects.filter(book_recommened=True)
        elif query == 'highranked':
            books = get_list_or_404(Book)
            serializer = BookListSerializer(books, many=True)
            sorted_data = sorted(serializer.data, key=lambda x: x['book_customer_review_rank'], reverse=True)
            return Response(sorted_data)
        elif query == 'userRecommended':
            user = request.user
            # thread 별로 작성된 점수로 weighted avg 계산
            threads = user.thread_set.all()
            total_weights = 0
            embedding = None
            if user.thread_set.count() != 0:
                for thread in threads:
                    weight = thread.thread_book_review_rank + 1
                    raw_embedding = thread.book.book_embedding
                    if raw_embedding:
                        temp = np.array(json.loads(raw_embedding))
                        if embedding is None:
                            embedding = weight * temp
                        else:
                            embedding = np.add(embedding, weight * temp)
                        total_weights += weight
                if total_weights == 0:
                    print('유효한 embedding이 없습니다...')
                    books = get_list_or_404(Book)
                    serializer = BookListSerializer(books, many=True)
                    sorted_data = sorted(serializer.data, key=lambda x: x['book_customer_review_rank'])
                    resp = {
                        'data': sorted_data,
                        'success': False,
                    }
                    return Response(resp)
                embedding /= total_weights
                books = get_list_or_404(Book)
                recommended_books = sorted(books, key=lambda x: get_similarity(x.book_embedding, embedding), reverse=True)
                print(recommended_books)
                serializer = BookListSerializer(recommended_books[:10], many=True)
                resp = {
                    'data': serializer.data,
                    'success': True,
                }
                return Response(resp)
            else:
                books = get_list_or_404(Book)
                serializer = BookListSerializer(books, many=True)
                sorted_data = sorted(serializer.data, key=lambda x: x['book_customer_review_rank'])
                resp = {
                    'data': sorted_data,
                    'success': False,
                }
                return Response(resp)
            
        serializer = BookListSerializer(books, many=True)
        sorted_data = sorted(serializer.data, key=lambda x: x['book_customer_review_rank'])
        return Response(sorted_data)


@api_view(['GET'])
def book_detail(request, book_pk):
    if request.method == 'GET':
        book = get_object_or_404(Book, pk=book_pk)
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)


# thread views
@api_view(['GET'])
def thread_list(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'GET':
        threads = Thread.objects.filter(book=book)
        serializer = ThreadListSerializer(threads, many=True, context={'request': request})
        return Response(serializer.data)
        

@api_view(['POST'])
def thread_create(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    if request.method == 'POST':
        serializer = ThreadCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                cover_url = ai_instance.get_thread_image(request.data['thread_content'])
                buffer = BytesIO()
                response = requests.get(cover_url, stream=True)
                image = Image.open(response.raw)
                image.save(buffer, format='png')
                image_bytes = buffer.getvalue()
                thread = serializer.save(user=request.user, book=book)
                thread.thread_cover_img.save(f"{request.data['thread_title']}cover.jpg", ContentFile(image_bytes))
                thread.save()
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                print('ai banner를 만드는 데에 실패했습니다.')
                print(e)
            serializer.save(user=request.user, book=book)
            return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def thread_detail(request, book_pk, thread_pk):
    book = get_object_or_404(Book, pk=book_pk)
    thread = get_object_or_404(Thread, pk=thread_pk)
    if request.method == 'GET':
        serializer = ThreadDetailSerializer(thread)
        return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def thread_update_delete(request, book_pk, thread_pk):
    book = get_object_or_404(Book, pk=book_pk)
    thread = get_object_or_404(Thread, pk=thread_pk)
    if request.method == 'PUT':
        serializer = ThreadUpdateSerializer(thread, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def thread_like(request, book_pk, thread_pk):
    book = get_object_or_404(Book, pk=book_pk)
    thread = get_object_or_404(Thread, pk=thread_pk)
    if request.method == 'POST':
        if (request.user in thread.thread_like_users.all()):
            thread.thread_like_users.remove(request.user)
            result = {
                'liked' : False,
                'num_likes': thread.thread_like_users.count()
            }
            return Response(result)
        else:
            thread.thread_like_users.add(request.user)
            result = {
                'liked' : True,
                'num_likes': thread.thread_like_users.count()
            }
            return Response(result)

# comment views
@api_view(['GET'])
def comment_list(request, book_pk, thread_pk):
    print(thread_pk)
    thread = get_object_or_404(Thread, pk=thread_pk)
    comments = Comment.objects.filter(thread=thread)
    if request.method == 'GET':
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, thread=thread)
            return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def comment_create(request, book_pk, thread_pk):
    thread = get_object_or_404(Thread, pk=thread_pk)
    if request.method == 'POST':
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, thread=thread)
            return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def comment_like(request, book_pk, thread_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        if (request.user in comment.comment_like_users.all()):
            comment.comment_like_users.remove(request.user)
            result = {
                'liked' : False,
                'num_likes': comment.comment_like_users.count()
            }
            return Response(result)
        else:
            comment.comment_like_users.add(request.user)
            result = {
                'liked' : True,
                'num_likes': comment.comment_like_users.count()
            }
            return Response(result)
        


@api_view(['PUT', 'DELETE'])
def comment_update_delete(request, book_pk, thread_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'PUT':
        serializer = CommentUpdateSerializer(comment, data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_search_suggestions(request):
    query = request.GET.get('query', '')

    if not query:
        return JsonResponse([], safe=False)

    books = Book.objects.filter(
        Q(book_title__icontains=query) | Q(book_author__icontains=query)
    ).annotate(
        rank=Case(
            When(book_title__icontains=query, then=1),
            When(book_author__icontains=query, then=2),
            default=3,
            output_field=IntegerField()
        )
    ).order_by('rank', 'book_title')[:10]  # 필요하면 개수 제한

    results = [{'title': book.book_title, 'author': book.book_author} for book in books]
    return JsonResponse(results, safe=False)