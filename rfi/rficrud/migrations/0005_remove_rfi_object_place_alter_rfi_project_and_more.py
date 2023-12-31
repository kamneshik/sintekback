# Generated by Django 4.1.7 on 2023-04-07 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rficrud', '0004_rfi_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rfi',
            name='object_place',
        ),
        migrations.AlterField(
            model_name='rfi',
            name='project',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='rfi',
            name='rfi_number_from_akkuyu',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='rfi',
            name='status',
            field=models.CharField(choices=[('rejected', 'rejected'), ('accepted', 'accepted'), ('in process', 'in process'), ('canceled', 'canceled'), ('waiting for status', 'waiting for status')], default='waiting for status', max_length=20),
        ),
        migrations.CreateModel(
            name='Relation_Construction_Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(default='HZZ', max_length=10)),
                ('construction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rficrud.construction')),
            ],
        ),
        migrations.AddField(
            model_name='rfi',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rficrud.relation_construction_test'),
        ),
    ]
