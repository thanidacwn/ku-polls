# Generated by Django 4.1.3 on 2023-09-11 16:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0007_alter_question_pub_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="pub_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 11, 16, 35, 9, 858765, tzinfo=datetime.timezone.utc
                ),
                verbose_name="date published",
            ),
        ),
    ]
