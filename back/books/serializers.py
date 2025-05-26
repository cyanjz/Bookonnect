from rest_framework import serializers
from .models import Book, Author, Thread, Comment
from django.contrib.auth import get_user_model


# Books
class BookListSerializer(serializers.ModelSerializer):
    book_customer_review_rank = serializers.SerializerMethodField()

    def get_book_customer_review_rank(self, obj):
        threads = obj.thread_set.all()
        if len(threads) == 0:
            return 0
        else:
            score = 0
            count = 0
            for thread in threads:
                count += 1
                score += thread.thread_book_review_rank
        return round(score / count, 2)
    
    class Meta:
        model = Book
        fields = ['book_cover_img', 'book_title', 'book_customer_review_rank', 'pk']


class BookDetailSerializer(serializers.ModelSerializer):
    book_customer_review_rank = serializers.SerializerMethodField()

    def get_book_customer_review_rank(self, obj):
        threads = obj.thread_set.all()
        if len(threads) == 0:
            return 0
        else:
            score = 0
            count = 0
            for thread in threads:
                count += 1
                score += thread.thread_book_review_rank
        return round(score / count, 2)

    class BookDetailAuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Author
            fields = ['author_name',
                      'author_profile_img', 
                      'author_info', 
                      'author_info_mp3',
                      ]

    author = BookDetailAuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['book_title', 
                  'book_cover_img', 
                  'book_description', 
                  'book_ISBN13', 
                  'book_pub_date', 
                  'book_customer_review_rank',
                  'author', 
                  ]
        


# Threads
class ThreadListSerializer(serializers.ModelSerializer):
    class ThreadListUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ['username', 'user_profile_img']
    
    user = ThreadListUserSerializer(read_only=True)
    

    num_likes = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['thread_title', 
                  'thread_content', 
                  'thread_cover_img', 
                  'thread_book_review_rank', 
                  'num_likes', 
                  'num_comments', 
                  'liked', 
                  'user',
                  'pk',
                  ]
        

    def get_num_likes(self, obj):
        return obj.thread_like_users.count()
    
    def get_num_comments(self, obj):
        return obj.comment_set.count()
    
    def get_liked(self, obj):
        print(self.context)
        user = self.context["request"].user
        return obj.thread_like_users.filter(id=user.id).exists()
    

class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ['user', 'book', 'thread_cover_img', 'thread', 'thread_like_users']



# Comments
class CommentListSerializer(serializers.ModelSerializer):

    class CommentListUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ['username', 'user_profile_img', 'pk']

    
    user = CommentListUserSerializer(read_only=True)
    num_likes = serializers.SerializerMethodField(read_only=True)
    
    def get_num_likes(self, obj):
        return obj.comment_like_users.all().count()
    

    class Meta:
        model = Comment
        fields = ['pk', 
                  'comment_content', 
                  'comment_created_at', 
                  'comment_updated_at', 
                  'num_likes', 
                  'user',
                  ]

class ThreadDetailSerializer(serializers.ModelSerializer):
    class ThreadDetailUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ['username', 'user_profile_img', 'pk']

    class ThreadDetailCommentSerializer(serializers.ModelSerializer):
        num_likes = serializers.SerializerMethodField()

        def get_num_likes(self, obj):
            return obj.comment_like_users.all().count()

        class Meta:
            model = Comment
            fields = ['comment_content', 'comment_updated_at', 'num_likes']

    class ThreadDetailBookSerialzier(serializers.ModelSerializer):
        avg_review_rank = serializers.SerializerMethodField(read_only=True)

        def get_avg_review_rank(self, obj):
            temp = obj.thread_set.all()
            print(temp)
            result = sum(elem.thread_book_review_rank for elem in temp)/len(temp)
            return result

        class Meta:
            model = Book
            fields = ['book_title', 'book_cover_img', 'book_pub_date', 'avg_review_rank']

    comments = CommentListSerializer(read_only=True, many=True, source='comment_set')
    user = ThreadDetailUserSerializer(read_only=True)
    book = ThreadDetailBookSerialzier(read_only=True)

    class Meta:
        model = Thread
        fields = ['thread_title', 'thread_content', 'thread_book_review_rank', 'thread_updated_at', 'user', 'comments', 'book', 'thread_cover_img']
        read_only_fields = ['thread_updated_at']



        
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'thread', 'comment_content', ]
        read_only_fields = ['user', 'thread', ]


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_content']