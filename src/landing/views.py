from django.shortcuts import render

# Create your views here.
def home_page_view(request):
    print(request.session.get('project_handle'))
    return render(request, "landing/home.html", {})