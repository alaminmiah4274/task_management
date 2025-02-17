# Generated by Django 5.1.4 on 2025-01-30 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskdetail',
            name='assigned_to',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('COMPLETED', 'Completed'), ('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress')], default='PENDING', max_length=15),
        ),
    ]
