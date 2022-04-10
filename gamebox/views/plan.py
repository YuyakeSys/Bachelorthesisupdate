# -*- coding = utf-8 -*-
# @Time ： 2022/3/13 22:59
# @Author : M
# @File : plan.py
# @Software: PyCharm
import json
from datetime import datetime
import random

from django.http import JsonResponse
from django.shortcuts import render

from gamebox.models import PlanOrder, UserInfo
from gamebox.views.cart import get_Item, getUser


def subscribe_index(request):
    cartItems = get_Item(request)
    context = {
        'cartItems': cartItems,
    }
    return render(request, 'subscription_Info.html', context=context)


def plan_checkout(request, typeid):
    cartItems = get_Item(request)
    plan = ["monthly", "seasonally", "half-year", "annually", "lifelong"]
    price = [10, 28, 52, 80, 500]
    context = {
        'choice': plan[typeid],
        'price': price[typeid],
        'cartItems': cartItems,
    }
    return render(request, 'plan_checkout.html', context= context)


def processPlan(request):
    plan_data = ["monthly", "seasonally", "half-year", "annually", "lifelong"]
    # print('data', request.body)
    data = json.loads(request.body)
    plan_index = plan_data.index(data['form']['plan'])
    # print(plan_index)
    user = getUser(request)
    transaction_id = datetime.now().strftime("%Y%m%d") + str(random.randint(100, 999))
    order = PlanOrder.objects.create(transaction_id=transaction_id, plan=plan_index, customer_id=user.id)
    order.save()

    UserInfo.objects.filter(id=user.id).update(plan=plan_index, start_time=datetime.now().strftime("%Y-%m-%d"))
    return JsonResponse("complete", safe=False)
