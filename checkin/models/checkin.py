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
    sick1 = models.IntegerField(default=0)
    sick2 = models.IntegerField(default=0)
    sick3 = models.IntegerField(default=0)
    sick4 = models.IntegerField(default=0)
    sick5 = models.IntegerField(default=0)
    sick6 = models.IntegerField(default=0)
    sick7 = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
