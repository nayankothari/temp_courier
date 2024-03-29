# Generated by Django 4.1.4 on 2023-10-25 23:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0048_alter_complaints_message"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserBooking",
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
                ("s_name", models.CharField(blank=True, max_length=200, null=True)),
                ("s_mob", models.CharField(blank=True, max_length=200, null=True)),
                ("s_pincode", models.BigIntegerField(null=True)),
                ("s_address", models.TextField(blank=True, null=True)),
                ("r_name", models.CharField(blank=True, max_length=200, null=True)),
                ("r_mob", models.CharField(blank=True, max_length=200, null=True)),
                ("r_pincode", models.BigIntegerField(blank=True, null=True)),
                ("r_address", models.TextField(null=True)),
                ("p_weight", models.BigIntegerField(null=True)),
                ("p_lenght", models.CharField(blank=True, max_length=200, null=True)),
                ("p_breadth", models.CharField(blank=True, max_length=200, null=True)),
                ("p_hieght", models.CharField(blank=True, max_length=200, null=True)),
                ("p_item", models.TextField(blank=True, null=True)),
                ("p_remarks", models.TextField(blank=True, null=True)),
                (
                    "p_pickup",
                    models.DateTimeField(blank=True, max_length=200, null=True),
                ),
                ("status", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "office_message",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "assign_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name_plural": "User Booking",},
        ),
    ]
