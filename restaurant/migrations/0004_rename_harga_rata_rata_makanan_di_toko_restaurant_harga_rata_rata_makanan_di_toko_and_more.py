# Generated by Django 5.1.1 on 2024-10-24 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_alter_restaurant_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='Harga_Rata_Rata_Makanan_di_Toko',
            new_name='harga_rata_rata_makanan_di_toko',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='Jenis_Suasana',
            new_name='jenis_suasana',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='Nama_Restoran',
            new_name='nama_restoran',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='Preferensi_Makanan',
            new_name='preferensi_makanan',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='Rating_Toko',
            new_name='rating_toko',
        ),
        migrations.RenameField(
            model_name='restaurant',
            old_name='Variasi_Makanan',
            new_name='variasi_makanan',
        ),
    ]