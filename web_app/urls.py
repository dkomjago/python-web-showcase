from django.urls import path
from web_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('read', views.read, name='read'),
    path('post', views.post, name='post'),
    path('session', views.session, name='session'),
    path('find', views.search, name='search'),
]
