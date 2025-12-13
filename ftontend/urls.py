from django.urls import path

from . import views

urlpatterns = [
    path('api/chat/', views.chat_api, name='chat_api'),    
    path('', views.main_menu, name='main_menu'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('auth/', views.auth_view, name='auth'),
    path('universities/', views.course_view, name='course_view'),
    path('universities/<slug:slug>/', views.university_detail, name='university_detail'),
    path('videos/almaty-management-university/', views.video_detail, name='video_detail'),
    path('videos/nazarbayev-university/', views.video_detail2, name='video_detail2'),
    path('videos/kbtu/', views.video_detail3, name='video_detail3'),
]