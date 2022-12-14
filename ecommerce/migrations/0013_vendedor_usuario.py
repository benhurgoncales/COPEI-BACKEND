# Generated by Django 3.2.13 on 2022-11-07 03:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecommerce', '0012_auto_20221026_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendedor',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Logado'),
        ),
    ]
