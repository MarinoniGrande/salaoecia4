# Generated by Django 3.0.6 on 2020-09-03 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='status',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
