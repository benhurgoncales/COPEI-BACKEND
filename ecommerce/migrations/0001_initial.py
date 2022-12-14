# Generated by Django 3.2.13 on 2022-10-10 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CadastroFig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condicao', models.EmailField(max_length=50)),
                ('aceitaTroca', models.BooleanField(null=True)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={
                'verbose_name': 'Cadastro Figurinha',
                'verbose_name_plural': 'Cadastros das Figurinhas',
            },
        ),
        migrations.CreateModel(
            name='Estadio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomeEstadio', models.CharField(max_length=30, verbose_name='Nome do Estadio')),
            ],
            options={
                'verbose_name': 'Estadio',
                'verbose_name_plural': 'Estadios',
            },
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomeGrupo', models.CharField(max_length=1, verbose_name='Nome do Grupo')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('telefone', models.CharField(max_length=15)),
                ('estado', models.CharField(max_length=30)),
                ('cidade', models.CharField(max_length=30)),
                ('figcadastrada', models.ManyToManyField(to='ecommerce.CadastroFig', verbose_name='Figurinhas Cadastradas')),
            ],
            options={
                'verbose_name': 'Vendedor',
                'verbose_name_plural': 'Vendedores',
            },
        ),
        migrations.CreateModel(
            name='Selecao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pais', models.CharField(max_length=50, verbose_name='Insira o pais')),
                ('fotoBandeira', models.ImageField(max_length=255, null=True, upload_to='fotos')),
                ('fotoTime', models.ImageField(max_length=255, null=True, upload_to='fotos')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.grupo', verbose_name='Grupo')),
            ],
            options={
                'verbose_name': 'Seleção',
                'verbose_name_plural': 'Seleçoes',
            },
        ),
        migrations.CreateModel(
            name='Figurinha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(verbose_name='Numero Figurinha')),
                ('nomeFig', models.CharField(max_length=100, verbose_name='Nome da figurinha')),
                ('lendaria', models.BooleanField(null=True)),
                ('especial', models.BooleanField(null=True)),
                ('fotoFig', models.ImageField(max_length=255, upload_to='filmes')),
                ('estadio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.estadio', verbose_name='Estadio')),
                ('selecao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.selecao', verbose_name='Seleção')),
            ],
            options={
                'verbose_name': 'Figurinha',
                'verbose_name_plural': 'Figurinhas',
            },
        ),
        migrations.AddField(
            model_name='cadastrofig',
            name='figurinha',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.figurinha', verbose_name='Figurinha'),
        ),
    ]
