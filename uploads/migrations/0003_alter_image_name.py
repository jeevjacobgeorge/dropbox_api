# Generated by Django 5.0.7 on 2024-12-17 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0002_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
