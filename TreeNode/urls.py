# -*- coding: utf-8 -*-
"""
Time    : 2021/08/01 9:01 PM
Author  : huzing2524
Project : Django_MySQL_test
File    : urls.py
Url     : https://github.com/huzing2524/Django_MySQL_test
"""
from django.urls import path

from tree.views import IndexTreeView

urlpatterns = [
    path('index_tree', IndexTreeView.as_view())
]
