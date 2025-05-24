from django.db import models
from django.contrib.auth import get_user_model

PATH = {
    'Book' : {
        'cover_image' : 'books/book_covers/',
        'author_image' : 'books/author_images/',
        'audio_file' : 'books/audios/',
    },
    'Thread' : {
        'cover_image' : 'threads/thread_covers/',
    }
}


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=20)


class Book(models.Model):
    category = models.ForeignKey("books.Category", on_delete=models.CASCADE)
    author = models.ForeignKey("books.Author", on_delete=models.CASCADE)
    book_title = models.CharField(max_length=50)
    book_description = models.TextField()
    book_ISBN13 = models.CharField(max_length=50)
    book_cover_img = models.ImageField(upload_to=PATH['Book']['cover_image'], default='')
    book_publisher = models.CharField(max_length=50)
    book_pub_date = models.DateField()
    book_customer_review_rank = models.IntegerField(null=True)
    book_ranking = models.PositiveIntegerField()
    book_embedding = models.BinaryField(blank=True, null=True)


class Thread(models.Model):
    # user 회원 탈퇴 -> thread 삭제?
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)    # fk name -> model name
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)    # fk name -> model name
    thread_title = models.CharField(max_length=40)  # max_length 20 -> 40
    thread_content = models.TextField()
    thread_book_review_rank = models.FloatField(default=0.0)
    thread_cover_img = models.ImageField(upload_to=PATH['Thread']['cover_image'], default='')
    thread_created_at = models.DateTimeField(auto_now_add=True)
    thread_updated_at = models.DateTimeField(auto_now=True)
    # ThreadLikeUser -> thread_like_users
    thread_like_users = models.ManyToManyField(get_user_model(), related_name="user_like_threads")


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    thread = models.ForeignKey("books.Thread", on_delete=models.CASCADE)
    comment_content = models.TextField()
    comment_created_at = models.DateTimeField(auto_now_add=True)
    comment_updated_at = models.DateTimeField(auto_now=True)
    # CommentLikeUser -> comment_like_users
    comment_like_users = models.ManyToManyField(get_user_model(), related_name="user_like_comments")


class Author(models.Model):
    author_name = models.CharField(max_length=20)   # varchar(15) -> varchar(20)
    author_info = models.TextField()
    author_masterpeice = models.CharField(max_length=50)
    author_profile_img = models.ImageField(blank=True, upload_to=PATH['Book']['author_image'], default='')
    author_info_mp3 = models.FileField(blank=True, upload_to=PATH['Book']['audio_file'])