# Generated by Django 3.0.5 on 2020-06-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200611_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='ordernumber',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]