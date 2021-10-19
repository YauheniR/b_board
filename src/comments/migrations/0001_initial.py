# Generated by Django 3.2.8 on 2021-10-16 18:10
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bboard", "0002_additionalimage_bb"),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("author", models.CharField(max_length=30, verbose_name="Автор")),
                ("content", models.TextField(verbose_name="Содержание")),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="Выводить на экран?"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="Опубликовано"
                    ),
                ),
                (
                    "bb",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bboard.bb",
                        verbose_name="Обьявление",
                    ),
                ),
            ],
            options={
                "verbose_name": "Коментарий",
                "verbose_name_plural": "Коментарии",
                "ordering": ("created_at",),
            },
        ),
    ]
