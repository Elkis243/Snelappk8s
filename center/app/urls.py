from django.urls import path
from .views import *

urlpatterns = [
    path("create_subscribers/", Create_subscribers.as_view(), name="create_subscribers"),
    path("read_subscribers/", Read_subscribers.as_view(), name="read_subscribers"),
    path("paiement/", Paiement.as_view(), name="paiement"),
    path("update_invoice/<int:id_invoice>", Update_invoice.as_view(), name="update_invoice"),
    path("generate_pdf/<int:id_invoice>", Generate_invoice.as_view(), name="generate_pdf"),
]