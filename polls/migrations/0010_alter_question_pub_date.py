# Generated by Django 4.1.3 on 2023-09-13 09:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0009_alter_question_pub_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="pub_date",
            field=models.DateTimeField(
                default=django.utils.timezone.localtime, verbose_name="date published"
            ),
        ),
    ]