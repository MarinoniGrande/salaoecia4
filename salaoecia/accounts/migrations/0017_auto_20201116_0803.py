# Generated by Django 3.0.4 on 2020-11-16 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20201107_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='zip_code',
            field=models.CharField(max_length=20, null=True, verbose_name='CEP'),
        ),
    ]
