# Generated by Django 4.1.1 on 2022-09-25 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rasdel', models.CharField(max_length=500)),
                ('code', models.IntegerField()),
                ('review', models.IntegerField()),
                ('price', models.IntegerField()),
                ('rat', models.FloatField()),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
