from django.urls import path
from .views import *

urlpatterns = [
    path("", Connect.as_view(), name="connect"),
    path("disconnect", Disconnect.as_view(), name="disconnect")
]