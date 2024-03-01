"""
URL configuration for collabvault project.
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

from django.urls import path
from . import views

app_name='projects'
urlpatterns = [
    path("", views.project_list_view, name='list'),
    path("create/", views.project_create_view, name='create'),
    path("<slug:handle>/", views.project_detail_update_view, name='detail'),
    path("<slug:handle>/delete/", views.project_delete_view, name='delete'),
]