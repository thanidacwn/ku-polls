# Generated by Django 4.1.3 on 2023-09-07 07:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0004_question_available"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="pub_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 7, 7, 33, 47, 415614, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date published",
            ),
        ),
    ]
