# Generated by Django 4.1.7 on 2023-04-07 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0011_alter_rfi_test_rfi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfi',
            name='test_rfi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rficrud.relation_construction_test'),
        ),
    ]
