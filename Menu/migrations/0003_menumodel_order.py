# Generated by Django 4.1.7 on 2023-03-23 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0002_remove_menumodel_order_alter_menumodel_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menumodel',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Порядок'),
        ),
    ]
