# Generated by Django 5.2.3 on 2025-07-21 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_book_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.CharField(blank=True, default=' author', max_length=200),
            preserve_default=False,
        ),
    ]
