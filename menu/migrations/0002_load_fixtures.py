from django.db import migrations
from django.apps import apps
from django.core.management import call_command


def load_fixtures(apps, schema_editor):
    fixtures = ["dish", "menu", "menudish"]
    for fixture_name in fixtures:
        call_command('loaddata', fixture_name)


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_add_models'),
    ]

    operations = [
        migrations.RunPython(load_fixtures)
    ]
