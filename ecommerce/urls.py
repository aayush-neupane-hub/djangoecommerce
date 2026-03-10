from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('category/<category_slug>', views.category_views, name='category'),
    path('products', views.products_list, name='products'),
    path('contact', views.contact, name='contact'),
]
