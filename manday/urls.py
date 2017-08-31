"""WeWork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

app_name = "manday"
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<pk>[0-9]+)/$', views.PersonDetail.as_view(), name='person_detail'),
    url(r'^(?P<person_id>[0-9]+)/hours/add/$', views.add_hours, name='add_hours'),
    url(r'^(?P<manday_id>[0-9]+)/hours/delete/$', views.delete_hours, name='delete_hours'),
    url(r'^(?P<person_id>[0-9]+)/project/add/$', views.add_project_from_person, name='add_project_from_person'),
]
