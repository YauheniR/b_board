from bboard.form import SubRubricForm
from bboard.models import SubRubric
from bboard.models import SuperRubric
from django.contrib import admin


class SubRubricInLine(admin.TabularInline):
    model = SubRubric


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ("super_rubric",)
    inlines = (SubRubricInLine,)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
