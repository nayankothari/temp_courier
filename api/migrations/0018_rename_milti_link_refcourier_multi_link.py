# Generated by Django 4.1.4 on 2023-01-22 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0017_refcourier_multi_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="refcourier", old_name="milti_link", new_name="multi_link",
        ),
    ]
