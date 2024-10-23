# Generated by Django 5.1.1 on 2024-10-22 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourist_attraction', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='touristattraction',
            name='type',
        ),
        migrations.AddField(
            model_name='touristattraction',
            name='attraction_type',
            field=models.CharField(default='Unknown', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='gmapsurl',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='htmweekday',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='htmweekend',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='rating',
            field=models.FloatField(),
        ),
    ]
