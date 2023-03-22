"""Bachelor_thesis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from gamebox.views import home, account, device, user, cart, plan, game
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.home),
    path('user/profile', user.user_profile),

    path('login/', account.login),
    path('logout/', account.logout),
    path('register/', account.register),
    path('image/code/', account.image_code),


    path('device/index/', device.device_index),
    path('gameboxS/', device.gameboxS),
    path('gameboxXS/', device.gameboxXS),

    path('game/index/', game.game_list),
    path('game/<int:gid>/detail/', game.game_detail),
    path('cart/', cart.cart_list),
    path('cart/checkout/', cart.checkout_menu),
    path('update_item/', cart.updateItem, name="update_item"),
    path('processOrder/', cart.processOrder),
    path('game/comment/', game.comment_add),

    path('plan/index/', plan.subscribe_index),
    path('plan/checkout/<int:typeid>', plan.plan_checkout),
    path('processPlan/', plan.processPlan),

    path('intro/', home.info),
    path('QaA/', home.qaa),
    path('support/', home.support),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT},
            name='media'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, }),
]


handler404 = home.page_not_found
