from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.template import TemplateDoesNotExist
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.core.signing import BadSignature
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.views.generic import TemplateView
from bboard.form import ChangeUserInfoForm
from bboard.form import RegisterUserForm
from bboard.models import AdvUser
from bboard.utilities import signer


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
    return render(request, "bboard/profile.html")


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'bboard/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'bboard/user_is_activated.html'
    else:
        template = 'bboard/activation_done.html'
        user.is_activated = True
        user.is_active = True
        user.save()
    return render(request, template)


class BBLoginView(LoginView):
    template_name = "bboard/login.html"


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "bboard/logout.html"


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    form_class = ChangeUserInfoForm
    template_name = "bboard/change_user_info.html"
    success_url = reverse_lazy("bboard:profile")
    success_message = "Данные пользователя изменены"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = "bboard/password_change.html"
    success_url = reverse_lazy("bboard:profile")
    success_message = "Пароль пользователя изменен"


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'bboard/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('bboard:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'bboard/register_done.html'
