from django.urls import path
from .views import create_announcement, home, news_list, create_news, delete_response, user_responses, respond_to_announcement, edit_announcement, announcement_list, delete_announcement

urlpatterns = [
    path('', home, name='home'),
    path('announcement/create/', create_announcement, name='create_announcement'),
    path('announcement/edit/<int:pk>/', edit_announcement, name='edit_announcement'),
    path('announcements/', announcement_list, name='announcement_list'),
    path('announcement/delete/<int:pk>/', delete_announcement, name='delete_announcement'),
    path('announcement/<int:pk>/respond/', respond_to_announcement, name='respond_to_announcement'),
    path('user/responses/', user_responses, name='user_responses'),
    path('response/delete/<int:pk>/', delete_response, name='delete_response'),
    path('news/create/', create_news, name='create_news'),
    path('news/', news_list, name='news_list'),
]
