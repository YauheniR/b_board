from bboard.form import SubRubricForm
from bboard.models import AdditionalImage
from bboard.models import Bb
from bboard.models import SubRubric
from bboard.models import SuperRubric
from django.contrib import admin


class SubRubricInLine(admin.TabularInline):
    model = SubRubric


class AdditionalImageInLine(admin.TabularInline):
    model = AdditionalImage


class BbAdmin(admin.ModelAdmin):
    list_display = ("rubric", "title", "content", "author", "created_at")
    fields = (
        ("rubric", "author"),
        "title",
        "content",
        "price",
        "contacts",
        "image",
        "is_active",
    )
    inlines = (AdditionalImageInLine,)


class SuperRubricAdmin(admin.ModelAdmin):
    exclude = ("super_rubric",)
    inlines = (SubRubricInLine,)


class SubRubricAdmin(admin.ModelAdmin):
    form = SubRubricForm


admin.site.register(SuperRubric, SuperRubricAdmin)
admin.site.register(SubRubric, SubRubricAdmin)
admin.site.register(Bb, BbAdmin)
