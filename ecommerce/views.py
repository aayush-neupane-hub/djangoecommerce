from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db.models import Q

from django.core.paginator import Paginator

from . form import ContactForm
from .models import *

# Create your views here.

def index(request):
    search = request.GET.get('search')
    if search:
        data = Product.objects.filter(Q(name__icontains=search) 
                                      | Q(category__name__icontains=search))
        sendData={
            'products': data
        }
        return render(request, 'pages/search-list.html', sendData)
    else:
        data={
            'products':Product.objects.all()
        }
        return render(request, 'pages/index.html', data)


def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'pages/index.html')
        else:
            return render(request, 'pages/login.html')
    else:
        data={
            'form': AuthenticationForm()
        }
        return render(request, 'pages/login.html', data)

def user_logout(request):
    logout(request)
    return render(request, 'pages/index.html')


def register(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'pages/index.html')
        else:
            data={
                'form': form
            }
            return render(request, 'pages/register.html', data)
    else:
        data={
            'form': UserCreationForm()
        }
        return render(request, 'pages/register.html', data)
    


def contact(request):
        if request.method=="POST":
            form=ContactForm(request.POST)
            if form.is_valid():
                # form.save()
                return render(request, 'pages/index.html')
            else:
                data={
                    'form': form
                }
                return render(request, 'pages/contact.html', data)
        else:
            data={
                'form': ContactForm()
            }
            return render(request, 'pages/contact.html', data)  
        

def category_views(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    cat_id = category.id
    products = Product.objects.filter(category=cat_id)
    data={
        'products': products
    }
    return render(request, 'pages/category-products.html', data)


def products_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 3) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    data={
        'products': page_obj
    }
    return render(request, 'pages/products.html', data)