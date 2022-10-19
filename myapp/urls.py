from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('hello', views.hello_world),
    path('',views.home_page),
    path('task',views.test),
    path('all-analytics',views.all_analytics),
    
    path('<slug:short_url>',views.redirect_url),
    path('analytics/<slug:short_urls>',views.url_analytics)
]


