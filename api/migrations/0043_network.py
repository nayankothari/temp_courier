# Generated by Django 4.1.4 on 2023-07-16 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0042_booking_booking_mode_booking_mode_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="Network",
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
                ("pincode", models.BigIntegerField(blank=True, null=True)),
                (
                    "delivery_areas",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
                (
                    "non_delivery_area",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
                (
                    "chargeable_delivery_area",
                    models.TextField(blank=True, max_length=2000, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name_plural": "Network",},
        ),
    ]