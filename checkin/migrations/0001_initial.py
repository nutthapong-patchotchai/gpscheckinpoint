# Generated by Django 3.0.8 on 2020-07-19 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amphur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'อำเภอ',
                'verbose_name_plural': 'อำเภอ',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=150)),
                ('amphur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.Amphur')),
            ],
            options={
                'verbose_name': 'ตำบล',
                'verbose_name_plural': 'ตำบล',
            },
        ),
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'ภูมิภาค',
                'verbose_name_plural': 'ภูมิภาค',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=150)),
                ('geo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.Geography')),
            ],
            options={
                'verbose_name': 'จังหวัด',
                'verbose_name_plural': 'จังหวัด',
            },
        ),
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('post', models.TextField()),
                ('tel', models.TextField()),
                ('question1', models.IntegerField()),
                ('question2', models.IntegerField()),
                ('question3', models.IntegerField()),
                ('address2', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amphur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.Amphur')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.District')),
                ('geo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.Geography')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.Province')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'โปรไฟล์',
                'verbose_name_plural': 'โปรไฟล์',
            },
        ),
        migrations.CreateModel(
            name='point',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.FloatField(blank=True, default=0, null=True)),
                ('points2', models.FloatField(blank=True, default=0, null=True)),
                ('points3', models.FloatField(blank=True, default=0, null=True)),
                ('points4', models.FloatField(blank=True, default=0, null=True)),
                ('points5', models.FloatField(blank=True, default=0, null=True)),
                ('points6', models.FloatField(blank=True, default=0, null=True)),
                ('points7', models.FloatField(blank=True, default=0, null=True)),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'แต้มสะสม',
                'verbose_name_plural': 'แต้มสะสม',
            },
        ),
        migrations.CreateModel(
            name='gps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.TextField(blank=True, default=0, null=True)),
                ('longitude', models.TextField(blank=True, default=0, null=True)),
                ('sick1', models.IntegerField(default=0)),
                ('sick2', models.IntegerField(default=0)),
                ('sick3', models.IntegerField(default=0)),
                ('sick4', models.IntegerField(default=0)),
                ('sick5', models.IntegerField(default=0)),
                ('sick6', models.IntegerField(default=0)),
                ('sick7', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amphur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkin.Amphur')),
                ('geo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkin.Geography')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='checkin.Province')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'การเช็คอิน',
                'verbose_name_plural': 'การเช็คอิน',
            },
        ),
        migrations.AddField(
            model_name='district',
            name='geo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.Geography'),
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.Province'),
        ),
        migrations.AddField(
            model_name='amphur',
            name='geo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.Geography'),
        ),
        migrations.AddField(
            model_name='amphur',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='checkin.Province'),
        ),
    ]
