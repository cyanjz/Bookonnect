from django.shortcuts import render, get_list_or_404, get_object_or_404
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
                          CommentUpdateSerializer)
from .models import (Book, Thread, Comment)


# Create your views here.
# book views
@api_view(['GET'])
def book_list_create(request):
    if request.method == 'GET':
        books = get_list_or_404(Book)
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


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
        serializer = ThreadDetailSerializer(thread, data=request.data)
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



# 베스트 셀러 데이터를 받아오기 위한 view 함수
@api_view(['GET'])
def best_sellers(request):
    pass