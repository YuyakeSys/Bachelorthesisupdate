# -*- coding = utf-8 -*-
# @Time ： 2022/3/9 1:48
# @Author : M
# @File : account.py
# @Software: PyCharm
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO

from gamebox.utils.docode import check_code
from gamebox import models
from gamebox.utils.bootstrap import BootStrapForm
from gamebox.utils.encrypt import md5
from gamebox.utils.form import UserModelForm


class LoginForm(BootStrapForm):
    name = forms.CharField(
        label="username",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="PIN",
        widget=forms.TextInput,
        required=True
    )


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # {'username': 'wupeiqi', 'password': '123',"code":123}
        # {'username': 'wupeiqi', 'password': '5e5c3bad7eb35cba3638e145c830c35f',"code":xxx}

        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        print(form.cleaned_data)
        code = request.session.get('image_code', "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "Wrong PIN")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password", "Username or password error")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        request.session["info"] = {'id': user_object.id, 'name': user_object.name}
        # session可以保存7天
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    # 调用pillow函数，生成图片
    img, code_string = check_code()

    # 写入到自己的session中（以便于后续获取验证码再进行校验）
    request.session['image_code'] = code_string
    # 给Session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/')


def register(request):
    """ 注册 """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'register.html', {'form': form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        # {'username': 'wupeiqi', 'password': '123',"code":123}
        # {'username': 'wupeiqi', 'password': '5e5c3bad7eb35cba3638e145c830c35f',"code":xxx}

        # 验证码的校验
        name = form.cleaned_data["name"]
        print(form.cleaned_data)
        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        user_object = models.UserInfo.objects.filter(name=name).first()
        if user_object:
            form.add_error("password", "Username already in use")
            # form.add_error("username", "Username already in use")
            return render(request, 'register.html', {'form': form})

        # 用户名和密码正确
        # 网站生成随机字符串; 写到用户浏览器的cookie中；在写入到session中；
        form.save()
        user_object = models.UserInfo.objects.filter(name=name).first()
        request.session["info"] = {'id': user_object.id, 'name': user_object.name}
        request.session.set_expiry(60 * 60 * 24 * 7)
        redirect("/")
        # session可以保存7天
        return redirect('/')
    form.add_error("password", "Wrong password")
    return render(request, 'register.html', {'form': form})

