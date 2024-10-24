# Generated by Django 5.1.1 on 2024-10-24 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='atmosphere_type',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='average_price',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='food_preference',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='food_variations',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='name',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='rating',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='Harga_Rata_Rata_Makanan_di_Toko',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='Jenis_Suasana',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='Nama_Restoran',
            field=models.CharField(default='Unnamed Restaurant', max_length=255),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='Preferensi_Makanan',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='Rating_Toko',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='Variasi_Makanan',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
