# Generated by Django 5.2.1 on 2025-05-28 00:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "app_pjsell",
            "0003_remove_contato_dia_contato_data_m1_contato_data_m2_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="contato",
            name="data_m1",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
