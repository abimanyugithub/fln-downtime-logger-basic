# Generated by Django 4.2.16 on 2024-11-05 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AndonMesinApp', '0005_role_kategori'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='kategori',
            new_name='area_kerja',
        ),
    ]
