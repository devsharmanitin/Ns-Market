# Generated by Django 4.2.3 on 2023-07-21 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('XMarket', '0004_color_alter_customuser_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Product_Color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='XMarket.color'),
        ),
    ]