# Generated by Django 4.1.7 on 2023-12-04 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticsScript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Webmaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
