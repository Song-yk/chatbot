# Generated by Django 5.0.6 on 2024-06-12 05:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chatgpt", "0005_document_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="content",
            field=models.TextField(blank=True),
        ),
    ]
