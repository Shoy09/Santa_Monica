# Generated by Django 5.0.1 on 2024-02-02 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_rename_creado_por_trabajosrealizados_creado_por_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trabajosrealizados',
            old_name='creado_por_user',
            new_name='creado_por',
        ),
    ]