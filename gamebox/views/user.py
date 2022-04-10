# -*- codeing = utf-8 -*-
# @Time ： 2022/3/9 1:41
# @Author : M
# @File : user.py
# @Software: PyCharm
from django.shortcuts import render, redirect
import datetime

from gamebox import models
from gamebox.models import List, PlanOrder
from gamebox.utils.pagination import Pagination
from gamebox.views.cart import getUser, get_Item


def user_profile(request):
    cartItems = get_Item(request)
    user_object = getUser(request)
    plan_data = user_object.plan
    plan_date = user_object.start_time
    today = datetime.date.today()
    if plan_data == 0:
        status = 'expired'
    elif plan_data == 1:
        date2 = plan_date + datetime.timedelta(days=30)
        if date2 >= today:
            status = 'active'
        else:
            status = 'expired'
    elif plan_data == 2:
        date2 = plan_date + datetime.timedelta(days=30 * 3)
        if date2 >= today:
            status = 'active'
        else:
            status = 'expired'
    elif plan_data == 3:
        date2 = plan_date + datetime.timedelta(days=30 * 6)
        if date2 >= today:
            status = 'active'
        else:
            status = 'expired'
    elif plan_data == 4:
        date2 = plan_date + datetime.timedelta(days=30 * 12)
        if date2 >= today:
            status = 'active'
        else:
            status = 'expired'
    elif plan_data == 5:
        status = 'active'
    game_order = List.objects.filter(customer_id=user_object.id, complete=1).all()
    plan_order = PlanOrder.objects.filter(customer_id=user_object.id)
    context = {
        'game_order': game_order,
        'plan_order': plan_order,
        'cartItems': cartItems,
        'status': status,
        'user_object': user_object,
    }
    return render(request, 'user_profile.html', context)


