# Generated by Django 4.1.4 on 2023-10-29 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0050_userbooking_ip_address_userbooking_pick_up_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userbooking",
            name="branch_aloted",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]