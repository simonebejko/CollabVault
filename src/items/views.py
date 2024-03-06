from django.contrib.admin.views.decorators import staff_member_required as login_required
from django.shortcuts import render, get_object_or_404, redirect
from . import forms
from .models import Item
from projects.decorators import project_required
from django.urls import reverse
from collabvault import http
from django.http import QueryDict, HttpResponse, JsonResponse
import s3
import pathlib
from collabvault.env import config
import mimetypes
from django_htmx.http import HttpResponseClientRedirect
from django.utils.text import slugify

AWS_ACCESS_KEY_ID=config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY=config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_BUCKET_NAME=config("AWS_BUCKET_NAME", default=None)

# Create your views here.
def filename_to_s3_filename(fname):
    if fname is None:
        return None
    if fname == '':
        return None
    stem = pathlib.Path(fname).stem
    suffix = pathlib.Path(fname).suffix
    stem_clean = slugify(stem).replace('-', '_')
    return f'{stem_clean}{suffix}'

@project_required
@login_required
def item_upload_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    template_name = 'items/file-upload.html'
    if request.htmx:
        template_name = 'items/snippets/upload.html'
    if request.method == "POST":
        print(request.POST)
        file_name = request.POST.get('file_name')
        name = filename_to_s3_filename(file_name)
        if name is None:
            """
            Invalid name, alert user
            """
            return JsonResponse({"url": None})
        client = s3.S3Client(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            default_bucket_name=AWS_BUCKET_NAME,
        ).client
        prefix = instance.get_prefix()
        key = f"{prefix}{name}"
        url = client.generate_presigned_url('put_object', Params={"Bucket": AWS_BUCKET_NAME, "Key": key}, ExpiresIn=3600)
        return JsonResponse({"url": url, 'filename': name})
    return render(request, template_name, 
                    {
                     "instance": instance}
                )

@project_required
@login_required
def item_file_delete_view(request, id=None, name=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    if not request.htmx:
        detail_url = instance.get_absolute_url()
        return redirect(detail_url)
    if request.method != "POST":
        detail_url = instance.get_absolute_url()
        return HttpResponseClientRedirect(detail_url)
    prefix = instance.get_prefix()
    client = s3.S3Client(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            default_bucket_name=AWS_BUCKET_NAME,
        ).client
    prefix = instance.get_prefix()
    key = f"{prefix}{name}"
    if key.endswith("/"):
        key = key[:-1]
    client.delete_object(Bucket=AWS_BUCKET_NAME, Key=key)
    return HttpResponse(f"{name} Deleted")

@project_required
@login_required
def item_files_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    if not request.htmx:
        detail_url = instance.get_absolute_url()
        return redirect(detail_url)
    template_name = 'items/snippets/object-table.html'
    prefix = instance.get_prefix()
    client = s3.S3Client(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            default_bucket_name=AWS_BUCKET_NAME,
        ).client

    paginator = client.get_paginator("list_objects_v2")
    pag_gen = paginator.paginate(
            Bucket=AWS_BUCKET_NAME,
            Prefix=prefix
    )
    object_list = []
    for page in pag_gen:
        #print(page.get('Contents'))
        for c in page.get('Contents', []):
            key = c.get('Key')
            size = c.get('Size')
            if size == 0:
                continue
            name = pathlib.Path(key).name
            _type = None
            try:
                _type = mimetypes.guess_type(name)[0]
            except:
                pass
            url = client.generate_presigned_url(
                'get_object',
                Params = {
                    'Bucket': AWS_BUCKET_NAME,
                    'Key': key,
                },
                ExpiresIn=3600,
            )
            download_url = client.generate_presigned_url(
                'get_object',
                Params = {
                    'Bucket': AWS_BUCKET_NAME,
                    'Key': key,
                    'ResponseContentDisposition': 'attachment'
                },
                ExpiresIn=3600,
            )
            is_image = 'image' in str(_type)
            updated = c.get('LastModified')
            data = {
                'key': key,
                'name': pathlib.Path(key).name,
                'is_image': is_image,
                'url': url,
                'download_url': download_url,
                'type': _type,
                'size': size,
                'updated': updated,
            }
            object_list.append(data)
    return render(request, template_name, {'object_list': object_list, "instance": instance})

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
def item_detail_inline_update_view(request, id=None):
    instance = get_object_or_404(Item, id=id, project=request.project)
    if not request.htmx:
        detail_url = instance.get_absolute_url()
        return redirect(detail_url)   
    template_name = "items/snippets/table-row-edit.html"
    success_template = "items/snippets/table-row.html"
    if f"{request.method}".lower() == "patch":
        query_dict = QueryDict(request.body)
        data = query_dict.dict()
        form = forms.ItemPatchForm(data)
        if form.is_valid():
            valid_data = form.cleaned_data
            changed = False
            for k, v in valid_data.items():
                changed = True
                if v == "":
                    continue
                if not v:
                    continue
                setattr(instance, k , v)
            if changed:
                instance.save()
        template_name = success_template
        choices = Item.ItemStatus.choices
        context = {
            "instance": instance,
            "choices": choices,
            "form": form,
        }
        return render(request, template_name, context)
    
    form = forms.ItemInlineForm(request.POST or None, instance=instance)
    if form.is_valid():
        item_obj = form.save(commit=False)
        item_obj.last_modified_by = request.user 
        item_obj.save()
        template_name = success_template
    context = {
        "instance": instance,
        "form": form,
    }
    return render(request, template_name, context)

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
        if request.htmx:
            return http.render_refresh_list_view(request)
        return redirect("items:list")
    return render(request, "items/delete.html", {"instance": instance})

@project_required
@login_required
def item_create_view(request):
    template_name = 'items/create.html'
    if request.htmx:
        template_name = 'items/snippets/form.html'
    form = forms.ItemCreateForm(request.POST or None)
    if form.is_valid():
        item_obj = form.save(commit=False)
        item_obj.project = request.project
        item_obj.added_by = request.user
        item_obj.save()
        if request.htmx:
            return http.render_refresh_list_view(request)
        return redirect(item_obj.get_absolute_url())
    action_create_url = reverse("items:create")
    context = {
        "form": form,
        "btn_label": "Create item",
        "action_url": action_create_url
    }
    return render(request, template_name, context)