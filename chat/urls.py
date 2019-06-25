from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from chat.views import index
from django.urls import path

urlpatterns = [
    path('', index),
    url(r'^(?P<open_chat>\w+)/?$', index),
]