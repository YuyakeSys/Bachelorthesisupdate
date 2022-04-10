# -*- codeing = utf-8 -*-
# @Time ： 2022/3/19 14:26
# @Author : M
# @File : game.py
# @Software: PyCharm
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from gamebox.models import Game, Comment, UserInfo
from gamebox.utils.pagination import Pagination
from gamebox.views.cart import get_Item


class case:
    def __init__(self, gid, label):
        self.gid = gid
        self.label = label


def game_list(request):
    data_dict = {}
    cartItems = get_Item(request)
    search_data1 = request.GET.get('g', "")
    games = Game.objects.all()
    if search_data1:
        data_dict["name__icontains"] = search_data1
        games = Game.objects.filter(**data_dict).order_by("-id")
    types = [case(1, 'Sports'), case(2, 'action'), case(3, 'RolePlaying'), case(4, 'Adventure'), case(5, 'Simulation'),
             case(6, 'Strategy')]
    search_data2 = request.GET.get("type", '')
    if search_data2:
        games = Game.objects.filter(label=search_data2).all()
    page_object = Pagination(request, games)
    page_string = page_object.html()
    context = {
        'games': page_object.page_queryset,
        'cartItems': cartItems,
        "page_string": page_string,
        'types': types
    }
    return render(request, 'game_list.html', context)


def game_detail(request, gid):
    game = Game.objects.filter(id=gid).first()
    game.views += 1
    game.save()
    name = game.name
    comments = Comment.objects.filter(game_id=name).all()
    postive = comments.filter(attitude=1).count()
    negative = comments.filter(attitude=2).count()
    if postive == 0 & negative == 0:
        status = "No comments yet"
    elif 0.9 * negative <= postive <= 1.1 * negative:
        status = "mixed"
    elif 1.1 * negative < postive:
        status = "Recommended"
    elif postive < 0.9 * negative:
        status = "Not Recommended"
    cartItems = get_Item(request)
    context = {
        'game_info': game,
        'cartItems': cartItems,
        'comments': comments,
        'status': status,
    }
    return render(request, 'game_detail.html', context)


@csrf_exempt
def comment_add(request):
    username = request.session['info']['name']
    user = UserInfo.objects.filter(name=username).first()
    game_name = request.POST.get('game')
    game = Game.objects.filter(name=game_name).first()
    attitude = request.POST.get('attitude')
    comment = request.POST.get('comment')
    if Comment.objects.filter(user=user, game=game).exists():
        data_dict = {"status": False}
        return HttpResponse(json.dumps(data_dict, ensure_ascii=False))

    Comment.objects.create(user=user, game=game, attitude=attitude, comment=comment)
    data_dict = {"status": True}
    return HttpResponse(json.dumps(data_dict))
