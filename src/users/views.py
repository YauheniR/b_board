from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from users.forms import ChangeUserInfoForm
from users.forms import RegisterUserForm
from users.forms import UsersPasswordResetForm
from users.models import AdvUser
from users.utilities import signer


@login_required
def profile(request):
    return render(request, "users/profile.html")


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, "users/bad_signature.html")
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = "users/user_is_activated.html"
    else:
        template = "users/activation_done.html"
        user.is_activated = True
        user.is_active = True
        user.save()
    return render(request, template)


class BBLoginView(LoginView):
    template_name = "users/login.html"


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "users/logout.html"


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    form_class = ChangeUserInfoForm
    template_name = "users/change_user_info.html"
    success_url = reverse_lazy("users:profile")
    success_message = "Данные пользователя изменены"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class BBPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = "users/password_change.html"
    success_url = reverse_lazy("users:profile")
    success_message = "Пароль пользователя изменен"


class BBPasswordResetView(PasswordResetView):
    form_class = UsersPasswordResetForm
    template_name = "users/password_reset.html"
    email_template_name = "email/password_reset_email.txt"
    success_url = reverse_lazy("users:password_reset_done")


class BBPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class BBPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class BBPasswordResetCompleteView(TemplateView):
    template_name = "users/password_reset_complete.html"


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = "users/register_user.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy("users:register_done")


class RegisterDoneView(TemplateView):
    template_name = "users/register_done.html"


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = "users/delete_user.html"
    success_url = reverse_lazy("bboard:index")

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, "Пользователь успешно удален!")
        return super().post(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
