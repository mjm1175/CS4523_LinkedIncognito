# Generated by Django 4.0.4 on 2022-04-19 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('Title', models.AutoField(primary_key=True, serialize=False)),
                ('JobType', models.CharField(max_length=20)),
                ('Description', models.CharField(max_length=1000)),
            ],
        ),
    ]
