"""inez_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.core.cache import cache
from django.contrib import admin
from django.urls import path
import INEZ.views as views
import os

urlpatterns = [
    path('_admin_/', admin.site.urls),
    path('', views.index, name="GroceryList"),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('item/<int:pk>/alt', views.item_alt, name="item-alt"),
    path('item/<int:pk>/edit', views.item_edit, name="item-edit")
]
