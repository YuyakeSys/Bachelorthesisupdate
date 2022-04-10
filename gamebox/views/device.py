from django.shortcuts import render
from gamebox.views.cart import get_Item


# -*- coding = utf-8 -*-
# @Time ： 2022/3/9 13:28
# @Author : M
# @File : device.py
# @Software: PyCharm
def device_index(request):
    cartItem = get_Item(request)
    return render(request, 'devices_list.html', {'cartItems': cartItem})


def gameboxS(request):
    cartItem = get_Item(request)
    return render(request, 'gamebox_s.html', {'cartItems': cartItem})
