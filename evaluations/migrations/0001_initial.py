# Generated by Django 5.0.7 on 2024-08-13 13:58

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('applicants', '0001_initial'),
        ('template', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_score', models.IntegerField(default=0)),
                ('is_submitted', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='applicants.application')),
                ('interviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('template', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='template.evaluationtemplate')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='evaluations.evaluation')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='template.evaluationquestion')),
            ],
        ),
    ]
