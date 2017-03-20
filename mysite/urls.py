"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from tamperProof import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adduser/', views.ui_add_user),
    url(r'^users/', views.ui_user_info),
    url(r'createuser/', views.add_user),
    url(r'deleteusers/', views.delete_users),
    url(r'addtask/', views.ui_add_task),
    url(r'selectsystem/', views.select_system),
    url(r'addnode/', views.add_node),
    url(r'processaddnode/', views.process_add_node),
    url(r'selectroot/', views.select_root),
    url(r'getsub/', views.get_sub),
]
