# Generated by Django 5.1.4 on 2025-02-18 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('COMPLETED', 'Completed'), ('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress')], default='PENDING', max_length=15),
        ),
    ]
