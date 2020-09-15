from django.db import models
from checkin.models.address import *

class Sizedorm(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class Zonedorm(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Pricedorm(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Typedorm(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Pet(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Makefood(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Dormitory(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    geo = models.ForeignKey(Geography, on_delete=models.CASCADE)
    amphur = models.ForeignKey(Amphur, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE) 
    post = models.TextField()
    tel = models.TextField()
    latitude = models.TextField(blank=True, null=True, default=0)
    longitude = models.TextField(blank=True, null=True, default=0)
    sizedorm =  models.ForeignKey(Sizedorm, on_delete=models.CASCADE)
    zonedorm =  models.ForeignKey(Zonedorm, on_delete=models.CASCADE)
    pricedorm =  models.ForeignKey(Pricedorm, on_delete=models.CASCADE)
    typedorm =  models.ForeignKey(Typedorm, on_delete=models.CASCADE)
    pet =  models.ForeignKey(Pet, on_delete=models.CASCADE)
    makefood =  models.ForeignKey(Makefood, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)