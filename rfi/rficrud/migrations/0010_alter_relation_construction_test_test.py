# Generated by Django 4.1.7 on 2023-04-07 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0009_alter_rfi_test_rfi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation_construction_test',
            name='test',
            field=models.CharField(default='HZZ', max_length=100),
        ),
    ]
