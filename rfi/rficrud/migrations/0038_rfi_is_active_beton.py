# Generated by Django 4.1.7 on 2023-05-10 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0037_alter_project_type_of_works'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfi',
            name='is_active_beton',
            field=models.BooleanField(default=False, help_text='Бетонирование'),
        ),
    ]
