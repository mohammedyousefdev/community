from django.urls import path
from .views import editPersonal, loginPage, logoutPage, profilePage, editProfilePage, questionsPage, registrationPage, answersPage, userPage


urlpatterns = [
    path("login", loginPage, name="login"),
    path("logout", logoutPage, name="logout"),
    path("registration", registrationPage, name="registration"),
    path("profile", profilePage, name="profile"),
    path("questions", questionsPage, name='questions'),
    path("answers", answersPage, name='answers'),
    path("edit-profile", editProfilePage, name="edit-profile"),
    path("edit-personal", editPersonal, name="edit-personal"),
    path("<str:username>/", userPage, name="user"),
]