# Generated by Django 4.1.7 on 2024-01-19 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_category_image_category_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='description',
            new_name='description2',
        ),
    ]
