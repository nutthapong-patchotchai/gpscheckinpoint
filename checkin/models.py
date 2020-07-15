from django.db import models


class gps(models.Model):
    latitude = models.FloatField(blank=True, null=True, default=0)
    longitude = models.FloatField(blank=True, null=True, default=0)
    sick1 = models.IntegerField(default=0)
    sick2 = models.IntegerField(default=0)
    sick3 = models.IntegerField(default=0)
    sick4 = models.IntegerField(default=0)
    sick5 = models.IntegerField(default=0)
    sick6 = models.IntegerField(default=0)
    sick7 = models.IntegerField(default=0)


class point(models.Model):
    points = models.FloatField(blank=True, null=True, default=0)
    points2 = models.FloatField(blank=True, null=True, default=0)
    points3 = models.FloatField(blank=True, null=True, default=0)
    points4 = models.FloatField(blank=True, null=True, default=0)
    points5 = models.FloatField(blank=True, null=True, default=0)
    points6 = models.FloatField(blank=True, null=True, default=0)
    points7 = models.FloatField(blank=True, null=True, default=0)
    status = models.IntegerField(default=0)
