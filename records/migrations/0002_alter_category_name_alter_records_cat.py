# Generated by Django 4.2.1 on 2025-03-14 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='records',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='posts', to='records.category', verbose_name='Категории'),
        ),
    ]
