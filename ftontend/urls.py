from django.urls import path

from . import views

urlpatterns = [
    path("", views.main_menu, name="main_menu"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
    path("universities/", views.course_view, name="course_view"),
    path("universities/<slug:slug>/", views.university_detail, name="university_detail"),
    path("videos/almaty-management-university/", views.video_detail, name="video_detail"),
    path("videos/nazarbayev-university/", views.video_detail2, name="video_detail2"),
    path("videos/kbtu/", views.video_detail3, name="video_detail3"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/register/", views.register_view, name="register"),
    path("account/delete/", views.delete_account_view, name="delete_account"),
]