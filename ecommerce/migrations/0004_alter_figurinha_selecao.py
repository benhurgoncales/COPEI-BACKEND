# Generated by Django 3.2.13 on 2022-10-20 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_alter_figurinha_selecao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='figurinha',
            name='selecao',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.PROTECT, to='ecommerce.selecao', verbose_name='Seleção'),
        ),
    ]