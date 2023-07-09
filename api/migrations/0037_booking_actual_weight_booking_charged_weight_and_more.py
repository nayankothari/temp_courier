# Generated by Django 4.1.4 on 2023-07-06 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0036_alter_cnotegenerator_from_range_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="actual_weight",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="charged_weight",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="declared_value",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="freight_charge",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="insurance_amt",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="insurance_per",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="pcs",
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="pod_charge",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="receiver_address",
            field=models.TextField(blank=True, default="", max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="sender_address",
            field=models.TextField(blank=True, default="", max_length=500, null=True),
        ),
        migrations.AddField(
            model_name="booking",
            name="spl_del_charge",
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
