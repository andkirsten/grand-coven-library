# Generated by Django 5.2.3 on 2025-07-21 02:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_city_book_publisher_book_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='class_code',
            new_name='book_type',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='type_code',
            new_name='magic_category',
        ),
    ]
