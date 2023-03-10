# Generated by Django 4.1.7 on 2023-02-20 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_load_fixtures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishmenu',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.dish'),
        ),
        migrations.AlterField(
            model_name='dishmenu',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.menu'),
        ),
    ]
