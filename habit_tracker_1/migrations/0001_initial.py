# Generated by Django 5.0.2 on 2025-03-28 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Habit",
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
                ("name", models.CharField(max_length=200)),
                ("completed", models.BooleanField(default=False)),
                ("date_completed", models.DateField(blank=True, null=True)),
                ("completion_count", models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
