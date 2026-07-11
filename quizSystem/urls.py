"""
URL configuration for onlineQuizSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from. import views

urlpatterns = [
    path('', views.quizSystem_index, name='quizSystem_index'),
    path('signup/', views.user_signup, name='user_signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quiz/', views.quiz_page, name='quiz_page'),
    path('save_user/', views.save_user, name='save_user'),
    path('tests/', views.tests, name='tests'),
    path('test/<int:test_id>/', views.start_test, name='start_test'),
]
