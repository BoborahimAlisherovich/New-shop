# Generated by Django 5.0.6 on 2024-05-28 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fruit', '0002_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(default=0.0004945598417408506, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.FloatField(default=4),
        ),
    ]
