# Generated by Django 3.0.2 on 2020-01-11 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='moderated',
            field=models.BooleanField(default=False, verbose_name='Прошло модерацию?'),
        ),
    ]
