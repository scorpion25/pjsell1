# Generated by Django 5.2.1 on 2025-05-28 22:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_pjsell", "0006_relatorioenvio"),
    ]

    operations = [
        migrations.AddField(
            model_name="relatorioenvio",
            name="cancelado",
            field=models.BooleanField(default=False),
        ),
    ]
