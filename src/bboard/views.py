from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template


def index(request):
    return render(request, "bboard/index.html")


def other_page(request, page):
    try:
        template = get_template("bboard/" + page + ".html")
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))
