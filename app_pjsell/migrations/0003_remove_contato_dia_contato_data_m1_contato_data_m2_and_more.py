# Generated by Django 5.2.1 on 2025-05-28 00:24

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_pjsell", "0002_contato_dia"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contato",
            name="dia",
        ),
        migrations.AddField(
            model_name="contato",
            name="data_m1",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="contato",
            name="data_m2",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contato",
            name="data_m3",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="contato",
            name="funcionario",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
