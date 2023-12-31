# Generated by Django 4.1.7 on 2023-04-12 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0026_alter_project_quality_plan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rfi',
            name='quality_plan_code',
        ),
        migrations.AlterField(
            model_name='project',
            name='quality_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rficrud.qualityplannumber'),
        ),
        migrations.AlterField(
            model_name='rfi',
            name='project_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rficrud.project'),
        ),
    ]
