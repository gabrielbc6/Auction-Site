# Generated by Django 3.2.8 on 2021-11-05 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lote', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leilao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicioLeilao', models.DateField()),
                ('finalLeilao', models.DateField()),
                ('maiorLance', models.CharField(max_length=200)),
                ('loteLeilao', models.CharField(max_length=200)),
                ('pagamentoLeilao', models.CharField(max_length=200)),
            ],
        ),
    ]
