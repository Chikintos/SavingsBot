# Generated by Django 4.1.7 on 2023-08-14 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('savingsApp', '0002_alter_operations_savings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operations',
            name='savings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savingsApp.savings'),
        ),
    ]
