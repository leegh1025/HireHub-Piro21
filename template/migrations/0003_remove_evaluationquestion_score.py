# Generated by Django 5.0.7 on 2024-08-04 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0002_rename_question_applicationquestion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluationquestion',
            name='score',
        ),
    ]
