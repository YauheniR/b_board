from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from users.apps import user_registered
from users.models import AdvUser


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Пароль (повторно)",
        widget=forms.PasswordInput,
        help_text="Введите тот же самый пароль еще раз для проверки",
    )

    def clean_password1(self):
        password1 = self.cleaned_data["password1"]
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        user = AdvUser.objects.filter(email=self.cleaned_data["email"])
        if user:
            errors = {
                "email": ValidationError(
                    "Пользователь с таким email уже зарегестрирован",
                    code="email_registered",
                )
            }
            raise ValidationError(errors)
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            errors = {
                "password2": ValidationError(
                    "Введенные пароли не совпадают", code="password_mismatch"
                )
            }
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_activated = False
        user.is_active = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "send_massages",
        )


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Адрес электронной почты")

    class Meta:
        model = AdvUser
        fields = ("username", "email", "first_name", "last_name", "send_massages")


class UsersPasswordResetForm(PasswordResetForm):
    def clean(self):
        super().clean()
        user = AdvUser.objects.filter(email=self.cleaned_data["email"])
        if not user:
            errors = {
                "email": ValidationError(
                    "Пользователь с таким email не зарегестрирован",
                    code="email_not_found",
                )
            }
            raise ValidationError(errors)


class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label="")
