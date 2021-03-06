# Generated by Django 4.0.2 on 2022-03-14 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=150)),
                ("description", models.TextField()),
                ("image", models.ImageField(upload_to="images")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="categories.category",
                    ),
                ),
                (
                    "similar_to",
                    models.ManyToManyField(
                        blank=True, default=None, to="categories.Category"
                    ),
                ),
            ],
        ),
    ]
