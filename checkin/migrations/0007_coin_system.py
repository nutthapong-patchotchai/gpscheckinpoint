from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("checkin", "0006_gps_place_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="gps",
            name="coin_awarded",
            field=models.BooleanField(default=False, verbose_name="ได้รับเหรียญแล้ว"),
        ),
        migrations.AddField(
            model_name="gps",
            name="coins_awarded",
            field=models.PositiveIntegerField(default=0, verbose_name="เหรียญที่ได้รับ"),
        ),
        migrations.AddField(
            model_name="gps",
            name="streak_day",
            field=models.PositiveIntegerField(default=0, verbose_name="จำนวนวันเช็คอินต่อเนื่อง"),
        ),
        migrations.AddField(
            model_name="cut_coin",
            name="activity_hours",
            field=models.DecimalField(
                decimal_places=1,
                default=0,
                max_digits=5,
                verbose_name="ชั่วโมงกิจกรรม",
            ),
        ),
        migrations.AddField(
            model_name="user_cut_coin",
            name="activity_hours",
            field=models.DecimalField(
                decimal_places=1,
                default=0,
                max_digits=5,
                verbose_name="ชั่วโมงกิจกรรมที่ได้รับ",
            ),
        ),
        migrations.AddField(
            model_name="user_cut_coin",
            name="balance_after",
            field=models.IntegerField(default=0, verbose_name="เหรียญคงเหลือหลังแลก"),
        ),
        migrations.AddField(
            model_name="user_cut_coin",
            name="coin_spent",
            field=models.PositiveIntegerField(default=0, verbose_name="เหรียญที่ใช้"),
        ),
        migrations.AddField(
            model_name="user_cut_coin",
            name="status",
            field=models.CharField(
                choices=[
                    ("approved", "อนุมัติแล้ว"),
                    ("pending", "รอตรวจสอบ"),
                    ("cancelled", "ยกเลิก"),
                ],
                default="approved",
                max_length=20,
                verbose_name="สถานะ",
            ),
        ),
        migrations.CreateModel(
            name="CoinWallet",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("balance", models.PositiveIntegerField(default=0, verbose_name="เหรียญคงเหลือ")),
                (
                    "current_streak",
                    models.PositiveIntegerField(default=0, verbose_name="เช็คอินต่อเนื่องปัจจุบัน"),
                ),
                (
                    "longest_streak",
                    models.PositiveIntegerField(default=0, verbose_name="เช็คอินต่อเนื่องสูงสุด"),
                ),
                (
                    "last_checkin_date",
                    models.DateField(blank=True, null=True, verbose_name="วันที่รับเหรียญล่าสุด"),
                ),
                ("total_earned", models.PositiveIntegerField(default=0, verbose_name="เหรียญที่ได้รับทั้งหมด")),
                ("total_spent", models.PositiveIntegerField(default=0, verbose_name="เหรียญที่ใช้ทั้งหมด")),
                (
                    "activity_hours",
                    models.DecimalField(
                        decimal_places=1,
                        default=0,
                        max_digits=7,
                        verbose_name="ชั่วโมงกิจกรรมที่แลกแล้ว",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="coin_wallet",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "กระเป๋าเหรียญ",
                "verbose_name_plural": "กระเป๋าเหรียญ",
            },
        ),
        migrations.CreateModel(
            name="CoinTransaction",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[
                            ("checkin", "เช็คอิน"),
                            ("redeem", "แลกชั่วโมงกิจกรรม"),
                            ("adjust", "ปรับยอด"),
                        ],
                        max_length=20,
                        verbose_name="ประเภท",
                    ),
                ),
                ("amount", models.IntegerField(verbose_name="จำนวนเหรียญ")),
                ("balance_after", models.IntegerField(verbose_name="เหรียญคงเหลือหลังรายการ")),
                ("streak_day", models.PositiveIntegerField(default=0, verbose_name="จำนวนวันเช็คอินต่อเนื่อง")),
                ("note", models.CharField(blank=True, default="", max_length=255, verbose_name="หมายเหตุ")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "checkin",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="coin_transactions",
                        to="checkin.gps",
                        verbose_name="รายการเช็คอิน",
                    ),
                ),
                (
                    "redemption",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="coin_transactions",
                        to="checkin.user_cut_coin",
                        verbose_name="รายการแลก",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="coin_transactions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wallet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions",
                        to="checkin.coinwallet",
                    ),
                ),
            ],
            options={
                "verbose_name": "ประวัติเหรียญ",
                "verbose_name_plural": "ประวัติเหรียญ",
                "ordering": ("-created_at",),
            },
        ),
    ]
