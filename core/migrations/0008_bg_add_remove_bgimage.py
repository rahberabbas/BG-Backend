# Generated by Django 4.2.1 on 2023-05-15 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_bg_add_color_b_remove_bg_add_color_g_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bg_add_remove',
            name='bgimage',
            field=models.URLField(blank=True, null=True),
        ),
    ]