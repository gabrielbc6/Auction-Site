# Generated by Django 3.2.9 on 2021-11-25 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lote', '0016_lote_pendente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='valorMinimo',
            field=models.FloatField(null=True),
        ),
    ]