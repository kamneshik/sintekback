# Generated by Django 4.1.7 on 2023-04-07 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0007_delete_proverka'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rfi',
            old_name='test',
            new_name='test_rfi',
        ),
    ]
