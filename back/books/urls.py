from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.book_list_create),
    path('<int:book_pk>/', views.book_detail),
    path('<int:book_pk>/threads/', views.thread_list),
    path('<int:book_pk>/threads/create/', views.thread_create),
    path('<int:book_pk>/threads/<int:thread_pk>/', views.thread_detail),
    path('<int:book_pk>/threads/<int:thread_pk>/update/', views.thread_update_delete),
    path('<int:book_pk>/threads/<int:thread_pk>/likes/', views.thread_like),
    path('<int:book_pk>/threads/<int:thread_pk>/comments/', views.comment_list),
    path('<int:book_pk>/threads/<int:thread_pk>/comments/create/', views.comment_create),
    path('<int:book_pk>/threads/<int:thread_pk>/comments/<int:comment_pk>/', views.comment_update_delete),
    path('<int:book_pk>/threads/<int:thread_pk>/comments/<int:comment_pk>/likes/', views.comment_like),

    # path('bestsellers/'.views.best_sellers),
]