# Generated by Django 4.2.10 on 2024-03-03 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_item__status_item_status_item_status_changed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='_status',
            field=models.CharField(blank=True, choices=[('publish', 'Published'), ('pending', 'Pending'), ('draft', 'Draft'), ('on_hold', 'On Hold')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('publish', 'Published'), ('pending', 'Pending'), ('draft', 'Draft'), ('on_hold', 'On Hold')], default='draft', max_length=20),
        ),
    ]
