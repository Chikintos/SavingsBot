# Generated by Django 4.1.7 on 2023-08-14 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('savingsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operations',
            name='savings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='savingsApp.savings'),
        ),
    ]