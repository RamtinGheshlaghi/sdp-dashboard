from django.shortcuts import render, get_object_or_404
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

    max_open_count = max([tech.open_count for tech in technician_stats], default=1)

    technician_chart = []
    for tech in technician_stats:
        technician_chart.append({
            "id": tech.id,
            "name": tech.name,
            "open_count": tech.open_count,
            "bar_width": int((tech.open_count / max_open_count) * 100) if max_open_count else 0,
        })

    context = {
        "open_tickets": Ticket.objects.filter(status="open").count(),
        "pending_tickets": Ticket.objects.filter(status="pending").count(),
        "overdue_tickets": Ticket.objects.filter(is_overdue=True).count(),
        "unassigned_tickets": Ticket.objects.filter(technician__isnull=True).count(),
        "open_ticket_list": open_ticket_list,
        "technician_stats": technician_stats,
        "technician_chart": technician_chart,
    }
    return render(request, "dashboard/home.html", context)


def technician_detail(request, pk):
    technician = get_object_or_404(Technician, pk=pk)

    tickets = (
        technician.tickets
        .all()
        .order_by("-created_at")
    )

    context = {
        "technician": technician,
        "tickets": tickets,
        "total_tickets": tickets.count(),
        "open_tickets": tickets.filter(status="open").count(),
        "pending_tickets": tickets.filter(status="pending").count(),
        "overdue_tickets": tickets.filter(is_overdue=True).count(),
        "closed_tickets": tickets.filter(status="closed").count(),
    }

    return render(request, "dashboard/technician_detail.html", context)

def ticket_list(request):
    tickets = (
        Ticket.objects
        .select_related("technician")
        .all()
        .order_by("-created_at")
    )

    context = {
        "tickets": tickets,
        "total_tickets": tickets.count(),
        "open_tickets": tickets.filter(status="open").count(),
        "pending_tickets": tickets.filter(status="pending").count(),
        "overdue_tickets": tickets.filter(is_overdue=True).count(),
    }

    return render(request, "dashboard/ticket_list.html", context)