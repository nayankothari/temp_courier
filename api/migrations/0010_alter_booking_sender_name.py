# Generated by Django 4.1.4 on 2023-01-14 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_booking_sender_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="sender_name",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
