# Generated by Django 4.1.7 on 2023-04-12 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0024_qualityplannumber_delete_qaqc_project_quality_plan'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='qualityplannumber',
            table='quality_plan_table',
        ),
    ]
