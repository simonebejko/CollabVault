from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from projects.models import Project, AnonymousProject
from django.contrib.admin.views.decorators import staff_member_required as login_required
from . import forms
from django.http import Http404

PROJECT_CAN_DELETE_ITEM_THRESHOLD = 3

# Create your views here.
def get_project_or_404(request, handle=None, skip_404=False):
    object_list = Project.objects.filter(handle=handle).has_access(request.user)
    if not object_list.exists() and not skip_404:
        raise Http404
    if not object_list.exists() and skip_404:
        return None
    return object_list.first() 

@login_required
def project_list_view(request):
    object_list = Project.objects.has_access(request.user)
    return render(request, "projects/list.html", {'object_list': object_list})

@login_required
def project_detail_update_view(request, handle=None):
    instance = get_project_or_404(request, handle=handle)
    items_qs = instance.item_set.all()
    form = forms.ProjectUpdateForm(request.POST or None, instance=instance)
    if form.is_valid():
        project_obj = form.save(commit=False)
        project_obj.last_modified_by = request.user 
        project_obj.save()
        return redirect(project_obj.get_absolute_url())
    context = {
        "instance": instance,
        "items_qs": items_qs,
        "form": form,
    }
    return render(request, "projects/detail.html", context)

@login_required
def project_delete_view(request, handle=None):
    instance = get_project_or_404(request, handle=handle)
    items_qs = instance.item_set.all()
    items_count = items_qs.count()
    items_exist = items_qs.exists()
    if request.method == 'POST':
        if items_exist and items_count >= PROJECT_CAN_DELETE_ITEM_THRESHOLD:
            messages.error(request, f"Cannot delete a project with {PROJECT_CAN_DELETE_ITEM_THRESHOLD} active items.")
            return redirect(instance.get_delete_url())
        instance.delete()
        return redirect("projects:list")
    return render(request, "projects/delete.html", {"instance": instance})

@login_required
def project_create_view(request):
    if not request.project.is_activated:
        return render(request, 'projects/activate.html', {})
    form = forms.ProjectCreateForm(request.POST or None)
    if form.is_valid():
        project_obj = form.save(commit=False)
        project_obj.owner = request.user
        project_obj.added_by = request.user
        project_obj.save()
        return redirect(project_obj.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, 'projects/create.html', context)

def delete_project_from_session(request):
    try:
        del request.session['project_handle']
    except:
        pass

def activate_project_view(request, handle=None):
    project_obj = get_project_or_404(request, handle=handle, skip_404=True)
    if project_obj is None:
        delete_project_from_session(request)
        messages.error(request, "Project could not activate. Try again.")
        return redirect("/projects")
    request.session['project_handle'] = handle
    messages.success(request, "Project activated.")
    return redirect("/")

def deactivate_project_view(request, handle=None):
    delete_project_from_session(request)
    messages.error(request, "Project deactivated.")
    return redirect("/")