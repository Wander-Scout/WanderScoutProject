# Generated by Django 5.1.1 on 2024-10-22 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourist_attraction', '0002_remove_touristattraction_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='touristattraction',
            name='latitude',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='touristattraction',
            name='longitude',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='touristattraction',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='attraction_type',
            field=models.CharField(default='General', max_length=255),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='description',
            field=models.TextField(default='No description available.'),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='gmapsurl',
            field=models.URLField(default='https://www.google.com/maps'),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='htmweekday',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='htmweekend',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='name',
            field=models.CharField(default='Unknown Attraction', max_length=255),
        ),
        migrations.AlterField(
            model_name='touristattraction',
            name='rating',
            field=models.FloatField(default=0.0),
        ),
    ]