# Generated by Django 4.1.4 on 2022-12-31 21:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0008_trackinghistory_remarks"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trackinghistory",
            name="in_out_datetime",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
