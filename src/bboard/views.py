from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404, HttpResponse
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


@login_required
def profile(request):
    return render(request, 'bboard/profile.html')


class BBLoginView(LoginView):
    template_name = 'bboard/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'bboard/logout.html'
