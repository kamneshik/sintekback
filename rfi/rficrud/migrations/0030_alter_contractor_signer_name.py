# Generated by Django 4.1.7 on 2023-04-24 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0029_alter_rfi_akkuyu_signer_alter_rfi_contractor_sintek_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='signer_name',
            field=models.CharField(default='-', max_length=200),
        ),
    ]
