from django.db import models

from django.contrib.auth.models import User
from checkin.models.address import *
from django.utils.translation import ugettext_lazy as _


class gps(models.Model):
    class Meta:
        verbose_name = _("การเช็คอิน")
        verbose_name_plural = _("การเช็คอิน")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.user.email

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
  etc = models.CharField(max_length=150,default="ไม่มีรายนะเอียด")
  status =  models.BooleanField(default=True,verbose_name="เปิดการใช้งาน")
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
  cut_coin = models.ForeignKey(cut_coin, on_delete=models.CASCADE,verbose_name="แลกแต้มสะสม")
  last_coin = models.FloatField(blank=True, null=True, default=0)
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


