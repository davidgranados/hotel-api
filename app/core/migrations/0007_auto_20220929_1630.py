# Generated by Django 3.2.15 on 2022-09-29 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_hotelroom_hotelroomreservation_reservationguestdetails_reservationinvoicedetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelroom',
            name='room_number',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='hotelroomreservation',
            unique_together={('room', 'check_in_date', 'check_out_date')},
        ),
    ]
