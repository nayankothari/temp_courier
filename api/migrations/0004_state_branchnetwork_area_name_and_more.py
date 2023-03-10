# Generated by Django 4.1.4 on 2023-01-04 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_branchnetwork_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="State",
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
                ("state_name", models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name="branchnetwork",
            name="area_name",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="branchnetwork",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="branchnetwork",
            name="state",
            field=models.ForeignKey(
                default="", on_delete=django.db.models.deletion.CASCADE, to="api.state"
            ),
        ),
    ]
