from bboard.models import AdditionalImage
from bboard.models import Bb
from bboard.models import SubRubric
from bboard.models import SuperRubric
from django import forms
from django.forms import inlineformset_factory


class BbForm(forms.ModelForm):
    class Meta:
        model = Bb
        fields = "__all__"
        widgets = {"author": forms.HiddenInput}


AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields="__all__")


class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(
        queryset=SuperRubric.objects.all(),
        empty_label=None,
        label="Надрубрика",
        required=True,
    )

    class Meta:
        model = SubRubric
        fields = "__all__"
