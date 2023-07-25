from django.urls import path
from .views import *

urlpatterns = [
    path("create_center/", Create_center.as_view(), name="create_center"),
    path("read_center/", Read_center.as_view(), name="read_center"),
    path("create_agent/", Create_agent.as_view(), name="create_agent"),
    path("read_agent/", Read_agent.as_view(), name="read_agent"),
    path("read_subscribers/", Read_subscribers.as_view(), name="read_subscribers"),
    path("create_invoice/", Create_invoice.as_view(), name="create_invoice"),
    path("paiement/", Paiement.as_view(), name="paiement"),
    path("update_invoice/<int:id_invoice>", Update_invoice.as_view(), name="update_invoice"),
    path("generate_pdf/<int:id_invoice>", Generate_invoice.as_view(), name="generate_pdf"),
]