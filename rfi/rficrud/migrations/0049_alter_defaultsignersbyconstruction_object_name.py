# Generated by Django 4.1.7 on 2023-05-24 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0048_rename_akkuyu_signer_name_relationakkuyurfi_signer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultsignersbyconstruction',
            name='object_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rficrud.construction', unique=True, verbose_name='Name of construction'),
        ),
    ]
