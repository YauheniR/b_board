from bboard.utilities import get_timestamp_path
from django.db import models
from users.models import AdvUser


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class Bb(models.Model):
    rubric = models.ForeignKey(
        "SubRubric", on_delete=models.PROTECT, verbose_name="Рубрика"
    )
    title = models.CharField(max_length=40, verbose_name="Товар")
    content = models.TextField(verbose_name="Описание")
    price = models.FloatField(default=0, verbose_name="Цена")
    contacts = models.TextField(verbose_name="Контакты")
    image = models.ImageField(
        blank=True, upload_to=get_timestamp_path, verbose_name="Изображение"
    )
    author = models.ForeignKey(
        AdvUser, on_delete=models.CASCADE, verbose_name="Автор обьявления"
    )
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name="Выводить в списке?"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Опубликовано"
    )

    def delete(self, using=None, keep_parents=False):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete()

    class Meta:
        verbose_name = "Обьявление"
        verbose_name_plural = "Обьявления"
        ordering = ("-created_at",)


class AdditionalImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name="Обьявление")
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name="Изображение")

    class Meta:
        verbose_name = "Дополнительная илюстрация"
        verbose_name_plural = "Дополнительные илюстрации"


class Rubric(models.Model):
    name = models.CharField(
        max_length=20, unique=True, db_index=True, verbose_name="Название"
    )
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name="Порядок")
    super_rubric = models.ForeignKey(
        "SuperRubric",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Надрубрика",
    )


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = (
            "order",
            "name",
        )
        verbose_name = "Надрубрика"
        verbose_name_plural = "Надрубрики"


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        return "%s - %s" % (self.super_rubric.name, self.name)

    class Meta:
        proxy = True
        ordering = (
            "super_rubric__order",
            "super_rubric__name",
            "order",
            "name",
        )
        verbose_name = "Подрубрика"
        verbose_name_plural = "Подрубрики"
