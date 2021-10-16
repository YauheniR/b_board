from bboard.models import Bb
from bboard.models import SubRubric
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from users.forms import SearchForm


def index(request):
    bbs = Bb.objects.filter(is_active=True)[:10]
    context = {"bbs": bbs}
    return render(request, "bboard/index.html", context)


def other_page(request, page):
    try:
        template = get_template("bboard/" + page + ".html")
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def by_rubric(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ""
    form = SearchForm(initial={"keyword": keyword})
    paginator = Paginator(bbs, 2)
    if "page" in request.GET:
        page_num = request.GET["page"]
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {"rubric": rubric, "page": page, "bbs": page.object_list, "form": form}
    return render(request, "bboard/by_rubric.html", context)


def detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {"bb": bb, "ais": ais}
    return render(request, "bboard/detail.html", context)
