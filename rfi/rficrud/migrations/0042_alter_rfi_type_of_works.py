# Generated by Django 4.1.7 on 2023-05-16 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0041_rfi_type_of_works_alter_rfi_excel_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfi',
            name='type_of_works',
            field=models.CharField(blank=True, choices=[('Kaynak', 'H-H-W-W'), ('Kaynak', 'H-H-R-R'), ('H-H-W-R', 'H-H-W-R'), ('Demir', 'H-H-H-H'), ('Default', 'H-W-W-W')], max_length=8, null=True, verbose_name='Точки из плана качества'),
        ),
    ]
