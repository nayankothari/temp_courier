# Generated by Django 4.1.4 on 2022-12-25 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_booking_ref_courier_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="c_note_number",
            field=models.BigIntegerField(unique=True),
        ),
    ]
