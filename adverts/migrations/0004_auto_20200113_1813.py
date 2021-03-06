# Generated by Django 3.0.2 on 2020-01-13 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0003_auto_20200111_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Удалено пользователем?'),
        ),
        migrations.AlterField(
            model_name='advert',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активно?'),
        ),
    ]
