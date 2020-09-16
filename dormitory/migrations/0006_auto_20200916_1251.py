# Generated by Django 3.0.8 on 2020-09-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dormitory', '0005_auto_20200916_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='DormOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='ชื่อ-สกุล')),
                ('type_owner', models.CharField(blank=True, choices=[('เจ้าของหอพักดูแลเอง', 'เจ้าของหอพักดูแลเอง'), ('แม่บ้าน / คนงานดูแล', 'แม่บ้าน / คนงานดูแล')], max_length=100, null=True, verbose_name='ชื่อ-สกุล')),
            ],
            options={
                'verbose_name': 'ผู้ประกอบการ',
                'verbose_name_plural': 'ผู้ประกอบการ',
            },
        ),
        migrations.AddField(
            model_name='dorm',
            name='advt',
            field=models.BooleanField(default=True, verbose_name='การเผยแพร่ข้อมูลหอพัก'),
        ),
        migrations.AddField(
            model_name='dorm',
            name='permission',
            field=models.BooleanField(default=True, verbose_name='การยินยอมให้ข้อมูลหอพักจากผู้ประกอบการ'),
        ),
    ]
