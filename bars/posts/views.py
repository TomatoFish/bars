# coding: utf-8

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Post
from .forms import PostForm


def post_create(request):
    if not request.user.is_authenticated():
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    if not request.user.is_active:
        return render(request, "post_list.html")
    else:
        fname = request.GET.get('filter')
        sname = request.GET.get('sort')
        query = request.GET.get('query')
        queryset_list = Post.objects.filter(user=request.user)

        catlist = []
        datelist = []
        for obj in queryset_list:
            if obj.category not in catlist:
                catlist.append(obj.category)
        for obj in queryset_list:
            if obj.publish not in datelist:
                datelist.append(obj.publish)

        if fname:
            if fname == "all":
                queryset_list = queryset_list.all()
            elif fname == "favourite":
                queryset_list = queryset_list.filter(favourite=True)
            elif fname[0] == "c":
                queryset_list = queryset_list.filter(category=fname[1:])
            else:
                queryset_list = queryset_list.filter(publish=fname)
        if query:
            queryset_list = queryset_list.filter(Q(title__icontains=query) |
                                                 Q(content__icontains=query)
                                                 ).distinct()
        if sname:
            queryset_list = queryset_list.order_by(sname)

        paginator = Paginator(queryset_list, 10)  # Show 25 contacts per page
        page_request_var = 'page'

        page = request.GET.get(page_request_var)
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of
            # results.
            queryset = paginator.page(paginator.num_pages)

        context = {
            "cat_list": catlist,
            "date_list": datelist,
            "object_list": queryset,
            "sort": sname,
            "filter": fname,
            "page_request_var": page_request_var
        }
        return render(request, "post_list.html", context)


def post_update(request, id=None):
    if not request.user.is_authenticated():
        raise Http404

    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    if not request.user.is_authenticated():
        raise Http404

    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")
