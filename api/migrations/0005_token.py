# Generated by Django 4.1.4 on 2023-01-08 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_state_branchnetwork_area_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Token",
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
                ("token", models.CharField(max_length=500)),
            ],
        ),
    ]