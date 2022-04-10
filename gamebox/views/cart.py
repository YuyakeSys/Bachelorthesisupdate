# -*- coding = utf-8 -*-
# @Time ： 2022/3/10 0:31
# @Author : M
# @File : cart.py
# @Software: PyCharm
import random

from django.shortcuts import render
from gamebox.models import UserInfo, List, Game, ListItem, Address
from django.http import JsonResponse
import json
from datetime import datetime

from gamebox.utils.pagination import Pagination


class case:
    def __init__(self, gid, label):
        self.gid = gid
        self.label = label


def cart_list(request):
    cartItems = get_Item(request)
    info_dict = request.session["info"]
    if info_dict:
        username = info_dict["name"]
        user = UserInfo.objects.filter(name=username).first()
        # cart list
        card_li, created = List.objects.get_or_create(customer=user, complete=False)
        items = card_li.listitem_set.all()
    else:
        item = []
        card_li = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'card_li': card_li, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def checkout_menu(request):
    cartItems = get_Item(request)
    user = getUser(request)
    card_li, created = List.objects.get_or_create(customer=user, complete=False)
    items = card_li.listitem_set.all()
    context = {'items': items, 'card_li': card_li, 'cartItems': cartItems}
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    gameId = data['gameId']
    action = data['action']
    user = getUser(request)
    game = Game.objects.get(id=gameId)
    order, created = List.objects.get_or_create(customer=user, complete=False)
    listItem, created = ListItem.objects.get_or_create(List=order, game=game)

    if action == 'add':
        listItem.quantity = (listItem.quantity + 1)
    elif action == 'remove':
        listItem.quantity = (listItem.quantity - 1)

    listItem.save()

    if listItem.quantity <= 0:
        listItem.delete()

    return JsonResponse('Item was added', safe=False)


# process the order and check whether total equals to total
def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(100, 999))
    user = getUser(request)
    total = float(data["form"]['total'])
    # print(total)
    order, created = List.objects.get_or_create(customer=user, complete=False)
    order.cost = total
    order.transaction_id = transaction_id
    # print(order.get_cart_total)
    if total == order.get_cart_total:
        order.complete = True
    # print(order.complete)
    order.save()

    Address.objects.create(
        user=user,
        order=order,
        address=data['shippingInfo']['address'],
        city=data['shippingInfo']['city'],
        state=data['shippingInfo']['state'],
        zipcode=data['shippingInfo']['zipcode'],
    )
    return JsonResponse("complete", safe=False)


def getUser(request):
    if "info" in request.session:
        info_dict = request.session["info"]
        username = info_dict["name"]
        user = UserInfo.objects.filter(name=username).first()
        return user
    else:
        return


def get_Item(request):
    if "info" in request.session:
        info_dict = request.session["info"]
        username = info_dict["name"]
        user = UserInfo.objects.filter(name=username).first()
        # cart list
        card_li, created = List.objects.get_or_create(customer=user, complete=False)
        items = card_li.listitem_set.all()
        cartItems = card_li.get_cart_items
    else:
        item = []
        card_li = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = card_li['get_cart_items']

    return cartItems


