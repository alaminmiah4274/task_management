# Generated by Django 5.1.4 on 2025-01-19 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_alter_taskdetail_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ManyToManyField(related_name='tasks', to='tasks.employee'),
        ),
    ]
