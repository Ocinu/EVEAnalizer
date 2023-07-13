# Generated by Django 4.2.3 on 2023-07-09 01:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("universe", "0004_remove_constellation_id_remove_region_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="article",
            name="id",
        ),
        migrations.RemoveField(
            model_name="category",
            name="id",
        ),
        migrations.RemoveField(
            model_name="group",
            name="id",
        ),
        migrations.AlterField(
            model_name="article",
            name="eve_id",
            field=models.PositiveIntegerField(
                editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="eve_id",
            field=models.PositiveIntegerField(
                editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="eve_id",
            field=models.PositiveIntegerField(
                editable=False, primary_key=True, serialize=False
            ),
        ),
    ]