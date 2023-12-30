# Generated by Django 4.1.7 on 2023-10-30 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_category_blog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='meta',
            new_name='meta_description',
        ),
        migrations.AddField(
            model_name='blog',
            name='meta_title',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
