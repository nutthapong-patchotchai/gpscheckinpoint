# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Geography(models.Model):
    class Meta:
        verbose_name = _("ภูมิภาค")
        verbose_name_plural = _("ภูมิภาค") 
    name = models.CharField(max_length=255)
    def __str__(self):
        return '{}'.format(self.name)


class Province(models.Model):
    class Meta:
        verbose_name = _("จังหวัด")
        verbose_name_plural = _("จังหวัด") 
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=150)
    geo = models.ForeignKey(Geography, on_delete=models.CASCADE)
    def __str__(self):
        return '{}'.format(self.name)


class Amphur(models.Model):
    class Meta:
        verbose_name = _("อำเภอ")
        verbose_name_plural = _("อำเภอ") 
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=150)
    geo = models.ForeignKey(Geography, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    def __str__(self):
        return '{}'.format(self.name)


class District(models.Model):
    class Meta:
        verbose_name = _("ตำบล")
        verbose_name_plural = _("ตำบล") 
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=150)
    amphur = models.ForeignKey(Amphur, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    geo = models.ForeignKey(Geography, on_delete=models.CASCADE)
    def __str__(self):
        return '{} > {}'.format(self.name, self.amphur.name)



 
