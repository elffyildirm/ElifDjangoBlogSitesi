# Generated by Django 3.0.5 on 2020-06-04 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200604_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
