from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from . import forms
from .models import Item
from projects import cache as projects_cache
from projects.decorators import project_required

# Create your views here.
@project_required
@login_required
def item_list_view(request):
    object_list = Item.objects.filter(project=request.project)
    template_name = "items/list.html"
    if request.htmx:
        template_name = "items/snippets/table.html"
    return render(request, template_name, {'object_list': object_list})

@project_required
@login_required
def item_detail_update_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    form = forms.ItemUpdateForm(request.POST or None, instance=instance)
    if form.is_valid():
        item_obj = form.save(commit=False)
        item_obj.last_modified_by = request.user 
        item_obj.save()
        return redirect(item_obj.get_absolute_url())
    context = {
        "instance": instance,
        "form": form,
    }
    return render(request, "items/detail.html", context)

@project_required
@login_required
def item_delete_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    if request.method == 'POST':
        instance.delete()
        return redirect("items:list")
    return render(request, "items/delete.html", {"instance": instance})

@project_required
@login_required
def item_create_view(request):
    form = forms.ItemCreateForm(request.POST or None)
    if form.is_valid():
        item_obj = form.save(commit=False)
        item_obj.project = request.project
        item_obj.added_by = request.user
        item_obj.save()
        projects_cache.get_user_projects(request.user.username)
        return redirect(item_obj.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, 'items/create.html', context)