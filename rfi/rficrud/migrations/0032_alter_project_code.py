# Generated by Django 4.1.7 on 2023-04-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0031_alter_project_code_alter_rfi_contractor_sintek_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.CharField(default=0, max_length=4),
        ),
    ]
