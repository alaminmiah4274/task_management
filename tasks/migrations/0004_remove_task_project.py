# Generated by Django 5.1.4 on 2025-02-18 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_status_alter_taskdetail_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='project',
        ),
    ]
