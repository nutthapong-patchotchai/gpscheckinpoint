from decimal import Decimal

from django.db import migrations


def seed_activity_rewards(apps, schema_editor):
    CutCoin = apps.get_model("checkin", "cut_coin")
    rewards = [
        {
            "title": "แลก 1 ชั่วโมงกิจกรรม",
            "coin": 100,
            "activity_hours": Decimal("1.0"),
            "etc": "ใช้สำหรับบันทึกชั่วโมงกิจกรรมทั่วไป",
        },
        {
            "title": "แลก 2 ชั่วโมงกิจกรรม",
            "coin": 180,
            "activity_hours": Decimal("2.0"),
            "etc": "เหมาะกับผู้ที่เช็คอินต่อเนื่องหลายวัน",
        },
        {
            "title": "แลก 5 ชั่วโมงกิจกรรม",
            "coin": 420,
            "activity_hours": Decimal("5.0"),
            "etc": "แพ็กใหญ่สำหรับผู้ที่สะสมเหรียญระยะยาว",
        },
    ]

    for reward in rewards:
        CutCoin.objects.update_or_create(
            title=reward["title"],
            defaults={
                "coin": reward["coin"],
                "activity_hours": reward["activity_hours"],
                "etc": reward["etc"],
                "status": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("checkin", "0007_coin_system"),
    ]

    operations = [
        migrations.RunPython(seed_activity_rewards, migrations.RunPython.noop),
    ]
