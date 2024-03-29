# Generated by Django 4.1.4 on 2023-07-15 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0040_remove_booking_gst_name_remove_booking_hsn_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="branchnetwork",
            name="contact_person",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="charged_weight",
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="weight",
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
