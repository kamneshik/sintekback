# Generated by Django 4.1.7 on 2023-04-12 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0027_remove_rfi_quality_plan_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type_of_works',
            field=models.CharField(choices=[('AR', 'AR'), ('AS', 'AS'), ('KZ', 'KZ'), ('KM', 'KM')], max_length=2),
        ),
    ]
