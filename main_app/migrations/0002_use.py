# Generated by Django 3.2.4 on 2021-07-08 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Use',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('drink', models.CharField(choices=[('C', 'Coffee'), ('T', 'Tea'), ('W', 'Hot Water'), ('H', 'Hot Cocoa'), ('O', 'Other')], default='C', max_length=1)),
                ('mug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.mug')),
            ],
        ),
    ]