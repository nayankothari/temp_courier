# Generated by Django 4.1.4 on 2023-12-09 17:32

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0053_messagemarquee_message1"),
    ]

    operations = [
        migrations.RemoveField(model_name="messagemarquee", name="message1",),
        migrations.AlterField(
            model_name="messagemarquee",
            name="message",
            field=ckeditor.fields.RichTextField(
                blank=True, default="", max_length=2000, null=True
            ),
        ),
    ]
