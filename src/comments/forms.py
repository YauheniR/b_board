from captcha.fields import CaptchaField
from comments.models import Comment
from django import forms


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ("is_active",)
        widgets = {"bb": forms.HiddenInput, "author": forms.HiddenInput}


class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(
        label="Введите текст с картинки",
        error_messages={"invalid": "Неправельный текст"},
    )

    class Meta:
        model = Comment
        exclude = ("is_active",)
        widgets = {"bb": forms.HiddenInput}
