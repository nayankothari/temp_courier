# Generated by Django 4.1.4 on 2023-08-04 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0044_contactus_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="e_way_bill_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="gst_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="payment_mode",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="remarks",
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="sender_mobile",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="branchnetwork",
            name="office_lane_line_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="contactus",
            name="mobile_number",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name="deliveryboymaster",
            name="alternate_number",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="deliveryboymaster",
            name="mobile_number",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="partyaccounts",
            name="mobile_number",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="partyaccounts",
            name="password",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="refcourier",
            name="type",
            field=models.CharField(
                choices=[("External", "External"), ("Internal", "Internal")],
                default="External",
                max_length=500,
            ),
        ),
        migrations.AlterField(
            model_name="useradditionaldetails",
            name="gst_number",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
