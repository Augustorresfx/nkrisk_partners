# Generated by Django 5.1.4 on 2025-01-16 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_pendingchange_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aseguradora',
            name='activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='broker',
            name='activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='matriz',
            name='activo',
            field=models.BooleanField(default=False),
        ),
    ]
