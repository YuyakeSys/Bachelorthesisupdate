from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from gamebox.models import Appeal
from gamebox.utils.form import QueryModelForm
from gamebox.utils.newsletter import sendMail
from gamebox.views.cart import get_Item, getUser


def home(request):
    email = request.GET.get('email', "")
    user = getUser(request)
    if User.email == email:
        sendMail("Subscribe successfully", user.name, user.email)
    elif email != "":
        sendMail("Subscribe successfully", user.name, email)
        user.email = email
        user.save()
    else:
        pass
    cartItems = get_Item(request)
    context = {
        'cartItems': cartItems,
    }
    return render(request, 'index.html', context=context)


def info(request):
    cartItems = get_Item(request)
    context = {
        'cartItems': cartItems,
    }
    return render(request, 'intro.html', context=context)


def qaa(request):
    cartItems = get_Item(request)
    context = {
        'cartItems': cartItems,
    }
    return render(request, 'qaa.html', context=context)


def support(request):
    cartItems = get_Item(request)
    if request.method == "GET":
        form = QueryModelForm()
        context = {
            'form': form,
            'cartItems': cartItems,
        }
        return render(request, 'query.html', context=context)
    form = QueryModelForm(data=request.POST)
    if form.is_valid():
        user = getUser(request)
        title = request.POST.get('title')
        issue = request.POST.get('issue')
        appeal = Appeal.objects.create(user=user,title=title,issue=issue)
        appeal.save()
        return redirect('/')
