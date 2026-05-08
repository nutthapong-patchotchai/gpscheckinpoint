from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("checkin", "0005_profile_faculty_gps_place_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="gps",
            name="place_address",
            field=models.TextField(blank=True, default="", verbose_name="ที่อยู่สถานที่"),
        ),
    ]
