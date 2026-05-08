from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("checkin", "0004_ensure_gps_district_column"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="faculty",
            field=models.CharField(blank=True, default="", max_length=160, verbose_name="คณะ"),
        ),
        migrations.AddField(
            model_name="gps",
            name="place_name",
            field=models.CharField(blank=True, default="", max_length=180, verbose_name="ชื่อสถานที่"),
        ),
    ]
