from django.urls import path, re_path
from . import views


urlpatterns = [
    path('index', views.testMenu, name = 'homepage'),
    path('about', views.testMenu, name = 'pageabout'),
    re_path(r'^.+', views.testMenu),
    path('', views.testMenu),


]
