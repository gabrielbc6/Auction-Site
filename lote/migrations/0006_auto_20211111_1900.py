# Generated by Django 3.2.8 on 2021-11-11 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lote', '0005_alter_lote_valorminimolance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leilao',
            name='maiorLance',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='lote',
            name='finalLeilao',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='lote',
            name='inicioLeilao',
            field=models.DateField(null=True),
        ),
    ]
