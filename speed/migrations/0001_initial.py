# Generated by Django 3.1 on 2020-11-15 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import speed.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('address', models.TextField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('slug', models.SlugField(allow_unicode=True, default='slug', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('qualf', models.TextField(max_length=100)),
                ('special', models.TextField(max_length=100)),
                ('contact_no', models.CharField(max_length=10)),
                ('register', models.BooleanField(default=False)),
                ('fees', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('clinic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctors', to='speed.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.PositiveSmallIntegerField()),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_number_verified', models.BooleanField(default=False)),
                ('change_pw', models.BooleanField(default=True)),
                ('phone_number', models.CharField(default=1, max_length=10, unique=True)),
                ('country_code', models.IntegerField(blank=True, default='+91')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='patient_profile', to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('objects', speed.manager.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MapDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=20)),
                ('near', models.BooleanField(default=False)),
                ('clinic', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rel_clinic', to='speed.clinic')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='membership', to='speed.doctor')),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_group', to='speed.patient')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='members',
            field=models.ManyToManyField(through='speed.GroupMember', to='speed.Patient'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('order_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('contact_no', models.CharField(default='Enter number', max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('subject', models.TextField(max_length=100)),
                ('delt', models.BooleanField(default=True)),
                ('deldoc', models.BooleanField(default=True)),
                ('pay_status', models.BooleanField(default=False)),
                ('doctor', models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, related_name='doc_appointments', to='speed.doctor')),
                ('patient', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='speed.patient')),
            ],
        ),
    ]
