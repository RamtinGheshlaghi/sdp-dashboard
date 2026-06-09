from django.shortcuts import render
from .models import Ticket


def home(request):
    open_ticket_list = (
        Ticket.objects
        .filter(status="open")
        .select_related("technician")
        .order_by("-created_at")
    )

    context = {
        "open_tickets": Ticket.objects.filter(status="open").count(),
        "pending_tickets": Ticket.objects.filter(status="pending").count(),
        "overdue_tickets": Ticket.objects.filter(is_overdue=True).count(),
        "unassigned_tickets": Ticket.objects.filter(technician__isnull=True).count(),
        "open_ticket_list": open_ticket_list,
    }
    return render(request, "dashboard/home.html", context)
