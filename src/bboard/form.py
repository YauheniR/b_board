from bboard.models import SubRubric
from bboard.models import SuperRubric
from django import forms


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
