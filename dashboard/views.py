from django.shortcuts import render

def home(request):
    context = {
        "open_tickets": 42,
        "pending_tickets": 11,
        "overdue_tickets": 7,
        "unassigned_tickets": 4,
    }
    return render(request, "dashboard/home.html", context)

