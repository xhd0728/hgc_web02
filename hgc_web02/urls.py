"""
URL configuration for hgc_web02 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("login/", views.login),
    path("index/", views.index),
    path("info/", views.info),

    path("update_pwd/", views.update_pwd),
    path("handle_pwd/", views.handle_pwd),

    path("page/", views.page),
    path("adv/", views.adv),
    path("book/", views.book),
    path("column/", views.column),

    path("list/", views.list_),
    path("add/", views.add),
    path("cate/", views.cate),

    path("handle_delete/", views.handle_delete),
    path("show_update/", views.show_update),
    path("handle_update/", views.handle_update),
    path("tips/", views.tips),
    path("sel_delete/", views.sel_delete),
    path("update_num/", views.update_num),
]
