"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import Feedback
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import models
from .models import Blog
from .models import Comment # использование модели комментариев
from .forms import CommentForm
from .forms import BlogForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def blog(request):
    """Renders the about page."""
    posts = Blog.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the about page."""
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей

            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
         form = CommentForm() # создание формы для ввода комментария
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            
            'post_1': post_1,
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведение о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Полезные ресурсы',
            'year':datetime.now().year,
        }
    )

def feedback(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1':'Мужчина', '2':'Женщина'}                 
    internet = {'1': '3-5', '2': '5-10',
                '3': '10-20','4': 'Больше 20'}
    if request.method == 'POST':
        form = Feedback(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['gender'] = gender [ form.cleaned_data['gender'] ]
            data['internet'] = internet [ form.cleaned_data['internet'] ]
            if(form.cleaned_data['notice'] == True):
                data ['notice'] = 'Да'
            else:   
                data ['notice'] = 'Нет'
            data ['email'] = form.cleaned_data['email']
            data ['message'] = form.cleaned_data['message']
            form = None
    else:
        form = Feedback()
    return render(
        request,
        'app/feedback.html',
        {
            'form':form,
            'data':data,
            'year':datetime.now().year
        }
    )

def registration(request):
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.data_foined = datetime.now()
            reg_f.last_login = datetime.now()

            regform.save()

            return redirect('home')
    else:
        regform = UserCreationForm()

    assert isinstance(request, HttpRequest)
    return render (
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year':datetime.now().year,
        }
    )

def newpost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save() # сохраняем изменения после добавления полей

            return redirect('blog') # переадресация на ту же страницу статьи после отправки комментария
    else:
         blogform = BlogForm()
 
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',         
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Наши видео',
            'year':datetime.now().year,
        }
    )