from datetime import timedelta

from django.db import models

from django.contrib.auth.models import User
from checkin.models.address import Amphur, District, Geography, Province
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class gps(models.Model):
    class Meta:
        verbose_name = _("การเช็คอิน")
        verbose_name_plural = _("การเช็คอิน")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=180, blank=True, default="", verbose_name="ชื่อสถานที่")
    place_address = models.TextField(blank=True, default="", verbose_name="ที่อยู่สถานที่")
    latitude = models.TextField(blank=True, null=True, default=0)
    longitude = models.TextField(blank=True, null=True, default=0)
    geo = models.ForeignKey(Geography, on_delete=models.CASCADE , blank=True, null=True)
    amphur = models.ForeignKey(Amphur, on_delete=models.CASCADE , blank=True, null=True )
    province = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, blank=True, null=True)  
    sick1 = models.IntegerField(default=0)
    sick2 = models.IntegerField(default=0)
    sick3 = models.IntegerField(default=0)
    sick4 = models.IntegerField(default=0)
    sick5 = models.IntegerField(default=0)
    sick6 = models.IntegerField(default=0)
    sick7 = models.IntegerField(default=0)
    coin_awarded = models.BooleanField(default=False, verbose_name="ได้รับเหรียญแล้ว")
    coins_awarded = models.PositiveIntegerField(default=0, verbose_name="เหรียญที่ได้รับ")
    streak_day = models.PositiveIntegerField(default=0, verbose_name="จำนวนวันเช็คอินต่อเนื่อง")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def full_name(self):
        return "%s %s"%(self.user.first_name, self.user.last_name)
    def geo_name(self):
        try:
          return "%s"%(self.geo.name)
        except:
          return "-"  
    def province_name(self):
        try:
          return "%s"%(self.province.name)
        except:
          return "-"   
    def amphur_name(self):
        try:
          return "%s"%(self.amphur.name)
        except:
          return "-"   
    def district_name(self):
        try:
          return "%s"%(self.district.name)
        except:
          return "-"
    @property
    def location_label(self):
        if self.place_name:
          return self.place_name
        parts = []
        if self.district:
          parts.append("ต.%s" % self.district.name)
        if self.amphur:
          parts.append("อ.%s" % self.amphur.name)
        if self.province:
          parts.append("จ.%s" % self.province.name)
        return " ".join(parts) or "-"

    def __str__(self):
        return self.user.email

class CoinWallet(models.Model):
    class Meta:
        verbose_name = _("กระเป๋าเหรียญ")
        verbose_name_plural = _("กระเป๋าเหรียญ")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="coin_wallet")
    balance = models.PositiveIntegerField(default=0, verbose_name="เหรียญคงเหลือ")
    current_streak = models.PositiveIntegerField(default=0, verbose_name="เช็คอินต่อเนื่องปัจจุบัน")
    longest_streak = models.PositiveIntegerField(default=0, verbose_name="เช็คอินต่อเนื่องสูงสุด")
    last_checkin_date = models.DateField(blank=True, null=True, verbose_name="วันที่รับเหรียญล่าสุด")
    total_earned = models.PositiveIntegerField(default=0, verbose_name="เหรียญที่ได้รับทั้งหมด")
    total_spent = models.PositiveIntegerField(default=0, verbose_name="เหรียญที่ใช้ทั้งหมด")
    activity_hours = models.DecimalField(
        max_digits=7,
        decimal_places=1,
        default=0,
        verbose_name="ชั่วโมงกิจกรรมที่แลกแล้ว",
    )
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def owner_name(self):
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return "%s - %s เหรียญ" % (self.owner_name, self.balance)

class point(models.Model):
    class Meta:
        verbose_name = _("แต้มสะสม")
        verbose_name_plural = _("แต้มสะสม")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.FloatField(blank=True, null=True, default=0)
    points2 = models.FloatField(blank=True, null=True, default=0)
    points3 = models.FloatField(blank=True, null=True, default=0)
    points4 = models.FloatField(blank=True, null=True, default=0)
    points5 = models.FloatField(blank=True, null=True, default=0)
    points6 = models.FloatField(blank=True, null=True, default=0)
    points7 = models.FloatField(blank=True, null=True, default=0)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return "%s %s"%(self.user.first_name, self.user.last_name)

#ฟังชั่นตัดcoin
class cut_coin(models.Model):
    class Meta:
        verbose_name = _("แลกแต้มสะสม")
        verbose_name_plural = _("แลกแต้มสะสม")

    title = models.CharField(max_length=150)
    coin = models.FloatField(blank=True, null=True, default=0)
    activity_hours = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="ชั่วโมงกิจกรรม")
    etc = models.CharField(max_length=150, default="ไม่มีรายนะเอียด")
    status = models.BooleanField(default=True, verbose_name="เปิดการใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


#ฟังชั่นตัดcoin user
class user_cut_coin(models.Model):
    class Meta:
        verbose_name = _("แลกแต้มสะสมของนิสิต")
        verbose_name_plural = _("แลกแต้มสะสมของนิสิต")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cut_coin = models.ForeignKey(cut_coin, on_delete=models.CASCADE, verbose_name="แลกแต้มสะสม")
    last_coin = models.FloatField(blank=True, null=True, default=0)
    coin_spent = models.PositiveIntegerField(default=0, verbose_name="เหรียญที่ใช้")
    activity_hours = models.DecimalField(max_digits=5, decimal_places=1, default=0, verbose_name="ชั่วโมงกิจกรรมที่ได้รับ")
    balance_after = models.IntegerField(default=0, verbose_name="เหรียญคงเหลือหลังแลก")
    status = models.CharField(
        max_length=20,
        default="approved",
        choices=(
            ("approved", "อนุมัติแล้ว"),
            ("pending", "รอตรวจสอบ"),
            ("cancelled", "ยกเลิก"),
        ),
        verbose_name="สถานะ",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cut_coin.title

    @property
    def full_name(self):
        return "%s %s"%(self.user.first_name, self.user.last_name)

    @property
    def coin_score(self):
        return "%s"%(self.cut_coin.coin)

    @property
    def coin(self):
        return "%s"%(self.cut_coin.title)


class CoinTransaction(models.Model):
    class Meta:
        verbose_name = _("ประวัติเหรียญ")
        verbose_name_plural = _("ประวัติเหรียญ")
        ordering = ("-created_at",)

    TYPE_CHECKIN = "checkin"
    TYPE_REDEEM = "redeem"
    TYPE_ADJUST = "adjust"

    TRANSACTION_TYPE_CHOICES = (
        (TYPE_CHECKIN, "เช็คอิน"),
        (TYPE_REDEEM, "แลกชั่วโมงกิจกรรม"),
        (TYPE_ADJUST, "ปรับยอด"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coin_transactions")
    wallet = models.ForeignKey(CoinWallet, on_delete=models.CASCADE, related_name="transactions")
    checkin = models.ForeignKey(
        gps,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="coin_transactions",
        verbose_name="รายการเช็คอิน",
    )
    redemption = models.ForeignKey(
        user_cut_coin,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="coin_transactions",
        verbose_name="รายการแลก",
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name="ประเภท",
    )
    amount = models.IntegerField(verbose_name="จำนวนเหรียญ")
    balance_after = models.IntegerField(verbose_name="เหรียญคงเหลือหลังรายการ")
    streak_day = models.PositiveIntegerField(default=0, verbose_name="จำนวนวันเช็คอินต่อเนื่อง")
    note = models.CharField(max_length=255, blank=True, default="", verbose_name="หมายเหตุ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s (%s)" % (self.user.username, self.amount, self.get_transaction_type_display())


class CovidCase(models.Model):
    class Meta:
        verbose_name = _("เคส COVID-19")
        verbose_name_plural = _("เคส COVID-19")
        ordering = ("-updated_at", "-created_at")

    STATUS_SUSPECTED = "suspected"
    STATUS_CONFIRMED = "confirmed"
    STATUS_RECOVERED = "recovered"
    STATUS_CLEARED = "cleared"

    STATUS_CHOICES = (
        (STATUS_SUSPECTED, "เฝ้าระวัง/สงสัยติดเชื้อ"),
        (STATUS_CONFIRMED, "ยืนยันติดเชื้อ"),
        (STATUS_RECOVERED, "หายแล้ว"),
        (STATUS_CLEARED, "ไม่พบเชื้อ/ปิดเคส"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="covid_cases", verbose_name="ผู้ใช้")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SUSPECTED,
        verbose_name="สถานะเคส",
    )
    symptom_started_on = models.DateField(blank=True, null=True, verbose_name="วันที่เริ่มมีอาการ")
    confirmed_on = models.DateField(blank=True, null=True, verbose_name="วันที่ตรวจพบ/ยืนยัน")
    trace_start_date = models.DateField(blank=True, null=True, verbose_name="เริ่มไล่ timeline")
    trace_end_date = models.DateField(blank=True, null=True, verbose_name="สิ้นสุดการไล่ timeline")
    notes = models.TextField(blank=True, default="", verbose_name="หมายเหตุ")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_covid_cases",
        verbose_name="ผู้บันทึกเคส",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def owner_name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def effective_trace_start_date(self):
        if self.trace_start_date:
            return self.trace_start_date

        date_candidates = [
            date_value
            for date_value in (self.symptom_started_on, self.confirmed_on)
            if date_value
        ]
        if date_candidates:
            return min(date_candidates) - timedelta(days=14)
        return timezone.localdate() - timedelta(days=14)

    @property
    def effective_trace_end_date(self):
        if self.trace_end_date:
            return self.trace_end_date
        return self.confirmed_on or timezone.localdate()

    @property
    def trace_window_label(self):
        return "%s - %s" % (
            self.effective_trace_start_date.strftime("%d/%m/%Y"),
            self.effective_trace_end_date.strftime("%d/%m/%Y"),
        )

    def __str__(self):
        return "%s (%s)" % (self.owner_name, self.get_status_display())
