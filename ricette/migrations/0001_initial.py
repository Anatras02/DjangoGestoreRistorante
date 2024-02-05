# Generated by Django 5.0.1 on 2024-02-01 16:23

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("ingredienti", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ricetta",
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
                ("nome", models.TextField()),
                ("descrizione", models.TextField()),
                (
                    "ingredienti",
                    models.ManyToManyField(
                        related_name="ricette", to="ingredienti.ingrediente"
                    ),
                ),
            ],
        ),
    ]
