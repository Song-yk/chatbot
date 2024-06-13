# accounts/urls.py

from django.urls import path
from .views import signup, user_login, user_logout

urlpatterns = [
    path('signup/', signup, name='signup'), # 회원가입 페이지
    path('login/', user_login, name='login'), # 회원가입 페이지
    path('logout/', user_logout, name='logout')
]
