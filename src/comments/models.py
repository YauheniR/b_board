from bboard.models import Bb
from comments.utilities import send_new_comment_notification
from django.db import models
from django.db.models.signals import post_save


class Comment(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name="Обьявление")
    author = models.CharField(max_length=30, verbose_name="Автор")
    content = models.TextField(verbose_name="Содержание")
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name="Выводить на экран?"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Опубликовано"
    )

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"
        ordering = ("created_at",)


def post_save_dispatcher(sender, **kwargs):
    author = kwargs["instance"].bb.author
    if kwargs["created"] and author.send_massages:
        send_new_comment_notification(kwargs["instance"])


post_save.connect(post_save_dispatcher, sender=Comment)
