from django.urls import path
from . import views

urlpatterns = [
    path("", views.my_view, name="my_view"),
    path("wacc_calculation/", views.wacc_view, name="wacc_view"),
]
