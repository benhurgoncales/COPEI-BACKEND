# Generated by Django 3.2.13 on 2022-10-26 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_alter_figurinha_numero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='figurinha',
            name='codigo',
        ),
        migrations.AddField(
            model_name='figurinha',
            name='num',
            field=models.IntegerField(null=True, verbose_name='Numero '),
        ),
        migrations.AlterField(
            model_name='figurinha',
            name='numero',
            field=models.CharField(max_length=20, null=True, verbose_name='Codigo Figurinha'),
        ),
    ]
