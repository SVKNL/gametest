# Generated by Django 5.0.7 on 2024-07-31 05:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('g', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='levelprize',
            name='player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='g.player'),
            preserve_default=False,
        ),
    ]
