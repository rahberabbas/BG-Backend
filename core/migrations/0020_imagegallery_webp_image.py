# Generated by Django 4.1.7 on 2024-01-20 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_rename_description_category_description2'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagegallery',
            name='webp_image',
            field=models.ImageField(blank=True, null=True, upload_to='webp_images/'),
        ),
    ]