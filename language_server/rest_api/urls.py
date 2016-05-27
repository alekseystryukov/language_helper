from django.conf.urls import url
from rest_api import views

urlpatterns = [
    url(r'^get_random_word/$', views.RandomWordApiView.as_view(),
        name="get_random_word"),
]
