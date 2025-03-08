"""
URL configuration for ocpp_backend project.

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
from django.contrib import admin
from django.urls import path
import chargers.views as views
urlpatterns = [
    path("chargers/", views.list_chargers, name="list_chargers"),
    path("remote_start/", views.remote_start_transaction, name="remote_start_transaction"),
    path("chargers/<str:charger_id>/status/", views.get_charger_status, name="charger_status"),
    path("get_logs/", views.get_logs, name="get_logs"),

]