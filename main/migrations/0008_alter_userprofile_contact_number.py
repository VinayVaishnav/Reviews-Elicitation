# Generated by Django 4.2.2 on 2023-07-28 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_poll_q1o4_poll_q2o4_poll_q3o4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='contact_number',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
