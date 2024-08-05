# Generated by Django 4.2.13 on 2024-08-03 05:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applicants", "0003_possible_date_list_application_interview_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="possible_date_list",
            name="max_possible_interview",
            field=models.IntegerField(default=0, verbose_name="면접타임개수"),
        ),
        migrations.AlterField(
            model_name="application",
            name="interview_time",
            field=models.TimeField(
                blank=True,
                choices=[
                    (None, "------"),
                    (datetime.time(9, 0), "09:00"),
                    (datetime.time(9, 30), "09:30"),
                    (datetime.time(10, 0), "10:00"),
                    (datetime.time(10, 30), "10:30"),
                    (datetime.time(11, 0), "11:00"),
                    (datetime.time(11, 30), "11:30"),
                    (datetime.time(12, 0), "12:00"),
                    (datetime.time(12, 30), "12:30"),
                    (datetime.time(13, 0), "13:00"),
                    (datetime.time(13, 30), "13:30"),
                    (datetime.time(14, 0), "14:00"),
                    (datetime.time(14, 30), "14:30"),
                    (datetime.time(15, 0), "15:00"),
                    (datetime.time(15, 30), "15:30"),
                    (datetime.time(16, 0), "16:00"),
                    (datetime.time(16, 30), "16:30"),
                    (datetime.time(17, 0), "17:00"),
                    (datetime.time(17, 30), "17:30"),
                ],
                null=True,
            ),
        ),
    ]
