from django.urls import path
from . import views

from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),

    ##########part2##########
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('security-question/', views.security_question_view, name='security_question'),
    path('show-reset-code/', views.show_reset_code, name='show_reset_code'),
    path('enter-reset-code/', views.enter_reset_code, name='enter_reset_code'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('reset/<str:token>/', views.reset_with_token, name='reset_with_token'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
]