# Generated by Django 5.0.4 on 2024-04-27 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'author'), (2, 'user')], db_index=True, default=2),
        ),
    ]
