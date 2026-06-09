from django.shortcuts import render
from django.db.models import Count, Q
from .models import Ticket, Technician


def home(request):
    open_ticket_list = (
        Ticket.objects
        .filter(status="open")
        .select_related("technician")
        .order_by("-created_at")
    )

    technician_stats = (
        Technician.objects
        .annotate(
            open_count=Count("tickets", filter=Q(tickets__status="open")),
            pending_count=Count("tickets", filter=Q(tickets__status="pending")),
            overdue_count=Count("tickets", filter=Q(tickets__is_overdue=True)),
            total_count=Count("tickets"),
        )
        .order_by("-open_count")
    )

    context = {
        "open_tickets": Ticket.objects.filter(status="open").count(),
        "pending_tickets": Ticket.objects.filter(status="pending").count(),
        "overdue_tickets": Ticket.objects.filter(is_overdue=True).count(),
        "unassigned_tickets": Ticket.objects.filter(technician__isnull=True).count(),
        "open_ticket_list": open_ticket_list,
        "technician_stats": technician_stats,
    }
    return render(request, "dashboard/home.html", context)