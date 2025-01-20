# -*- coding: utf-8 -*-

# from django.conf.urls import url
from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "transaction/completed/",
        views.TransactionCompletedView.as_view(),
        name="transaction_completed",
    ),
    path(
        "transaction/status/",
        views.TransactionStatusView.as_view(),
        name="transaction_status",
    ),
    path("transaction/ipn/", views.IPNCallbackView.as_view(), name="transaction_ipn"),
]
