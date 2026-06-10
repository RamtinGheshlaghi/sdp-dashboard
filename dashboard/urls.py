from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="dashboard_home"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("technicians/<int:pk>/", views.technician_detail, name="technician_detail"),
]