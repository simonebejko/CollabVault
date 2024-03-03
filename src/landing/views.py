from django.shortcuts import render
from items.models import Item
from projects.decorators import project_required

# Create your views here.
@project_required
def dashboard_view(request):
    qs = Item.objects.filter(project=request.project)
    return render(request, "dashboard/home.html", {"items": qs})

def home_page_view(request):
    if not request.user.is_authenticated:
        return render(request, "landing/home.html", {})
    return dashboard_view(request)

def about_page_view(request):
    print(request.project)
    return render(request, "landing/home.html", {})