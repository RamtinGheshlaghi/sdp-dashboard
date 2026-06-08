from django.shortcuts import render
from .models import Ticket

def home(request):
    context = {
        "open_tickets": Ticket.objects.filter(status="open").count(),
        "pending_tickets": Ticket.objects.filter(status="pending").count(),
        "overdue_tickets": Ticket.objects.filter(is_overdue=True).count(),
        "unassigned_tickets": Ticket.objects.filter(technician__isnull=True).count(),
    }
    return render(request, "dashboard/home.html", context)

