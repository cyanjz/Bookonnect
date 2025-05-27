from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('signup/', include('dj_rest_auth.registration.urls')),
    path('<int:user_pk>/', view=views.get_user_info),
    path('myinfo/', view=views.get_my_info),
    path('<int:user_pk>/follow/', view=views.follow),
    path('<int:user_pk>/update/', view=views.update_profile),
]