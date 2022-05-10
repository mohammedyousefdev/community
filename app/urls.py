from django.urls import path
from .views import createQuestion, homePage, singleQuestion

urlpatterns = [
    path("", homePage, name="home"),
    path("question-room/", createQuestion, name='question-room'),
    path("question/<str:pk>", singleQuestion, name='question')
]