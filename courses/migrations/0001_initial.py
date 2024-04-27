# Generated by Django 5.0.4 on 2024-04-27 10:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True)),
                ('description', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(10)])),
            ],
            options={
                'db_table': 'course',
            },
        ),
    ]
