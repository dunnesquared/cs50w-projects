# Generated by Django 2.0.3 on 2020-03-23 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_salad'),
    ]

    operations = [
        migrations.CreateModel(
            name='DinnerPlatter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('size', models.CharField(max_length=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]