# Generated by Django 4.2.1 on 2025-03-14 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0004_alter_records_options_records_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tag_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='records',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='records',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='records.category', verbose_name='Категории'),
        ),
        migrations.AlterField(
            model_name='tagpost',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tagposts', to=settings.AUTH_USER_MODEL),
        ),
    ]
