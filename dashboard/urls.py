from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="dashboard_home"),
    path("technicians/<int:pk>/", views.technician_detail, name="technician_detail"),
]