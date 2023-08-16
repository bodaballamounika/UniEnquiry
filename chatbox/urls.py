from django.urls import path

from . import views


urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('chat_list/', views.chat_list, name='chat_list'),
    path('chat_detail/<uuid:pk>/', views.chat_detail, name='chat_detail')
]
