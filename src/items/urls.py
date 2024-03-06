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

from django.urls import path, re_path
from . import views

app_name='items'
urlpatterns = [
    path("", views.item_list_view, name='list'),
    path("<int:id>/", views.item_detail_update_view, name='detail'),
    path("<int:id>/upload/", views.item_upload_view, name='upload'),
    path("<int:id>/files/", views.item_files_view, name='files'),
    re_path(r'^(?P<id>\d+)/files/(?P<name>.*)$', views.item_file_delete_view, name='files_delete'),
    path("<int:id>/edit/", views.item_detail_inline_update_view, name='edit'),
    path("<int:id>/delete/", views.item_delete_view, name='delete'),
    path("create/", views.item_create_view, name='create'),
]