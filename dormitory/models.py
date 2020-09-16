from django.db import models
from checkin.models.address import *
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField

class Choice(models.Model): 
    class Meta:
        verbose_name = _("จัดการประเภทตัวเลือก")
        verbose_name_plural = _("จัดการประเภทตัวเลือก") 
    ANSWERS = (
        ('การจดทะเบียนขออนุญาตผู้ประกอบกิจการหอพัก','การจดทะเบียนขออนุญาตผู้ประกอบกิจการหอพัก'),
        ('โซนหอพัก', 'โซนหอพัก'),
        ('ประเภทของหอพัก', 'ประเภทของหอพัก'),
        ('ลักษณะของหอพัก', 'ลักษณะของหอพัก'),
        ('ลักษณะการเข้าพักอาศัย', 'ลักษณะการเข้าพักอาศัย'),
        ('สิ่งอำนวยความสะดวกภายในหอพัก ', 'สิ่งอำนวยความสะดวกภายในหอพัก'),
        ('ระบบรักษาความปลอดภัย','ระบบรักษาความปลอดภัย'),
        ('ทำอาหารในหอพักได้หรือไม่','ทำอาหารในหอพักได้หรือไม่'),
        ('เลี้ยงสัตว์เลี้ยงในหอพักได้หรือไม่','เลี้ยงสัตว์เลี้ยงในหอพักได้หรือไม่'),
        ('การเผยแพร่ข้อมูลหอพัก','การเผยแพร่ข้อมูลหอพัก')
    )
    name =  models.CharField(max_length=100, choices=ANSWERS,verbose_name="ประเภทตัวเลือก" )
    value = models.CharField(max_length=100,verbose_name="ตัวเลือก")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s > %s"%(self.name, self.value)

 
class Dorm(models.Model):
    class Meta:
        verbose_name = _("ข้อมูลหอพัก")
        verbose_name_plural = _("ข้อมูลหอพัก")
    name = models.CharField(max_length=100,verbose_name="ชื่อหอพัก") 
    address = models.TextField(verbose_name="ที่อยู่")
    geo = models.ForeignKey(Geography, on_delete=models.CASCADE,verbose_name="ภูมิภาค")
    province = models.ForeignKey(Province, on_delete=models.CASCADE,verbose_name="จังหวัด") 
    amphur = models.ForeignKey(Amphur, on_delete=models.CASCADE,verbose_name="อำเภอ")
    district = models.ForeignKey(District, on_delete=models.CASCADE,verbose_name="ตำบล") 
    post = models.CharField(max_length=100,verbose_name="รหัสไปรศณีย์")
    tel = models.CharField(max_length=100,verbose_name="เบอร์โทร")
    latitude = models.CharField(max_length=100,blank=True, null=True, default=0)
    longitude = models.CharField(max_length=100,blank=True, null=True, default=0)  
    permission = models.BooleanField(default=True,verbose_name="การยินยอมให้ข้อมูลหอพักจากผู้ประกอบการ")
    advt = models.BooleanField(default=True,verbose_name="การเผยแพร่ข้อมูลหอพัก")
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} : {}'.format(self.name,self.address)

class DormDetail(models.Model):
    class Meta:
        verbose_name = _("ข้อมูลอื่นๆของหอพัก")
        verbose_name_plural = _("ข้อมูลอื่นๆของหอพัก")
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    build = models.IntegerField(default=0,verbose_name="จำนวนอาคาร")
    floor = models.IntegerField(default=0,verbose_name="จำนวนชั้น")
    room = models.IntegerField(default=0,verbose_name="จำนวนห้อง")  
    all_count = models.IntegerField(default=0,verbose_name="บรรจุผู้อาศัย รวมทั้งหมด")
    now_count = models.IntegerField(default=0,verbose_name="จำนวนนิสิตที่พักอาศัย ณ ปัจจุบัน")
    width = models.IntegerField(default=0,verbose_name="ความกว้าง")
    height =  models.IntegerField(default=0,verbose_name="ความยาว")

    fan_price_month = models.IntegerField(default=0,verbose_name="ห้องพัดลม รายเดือน ")
    fan_price_day = models.IntegerField(default=0,verbose_name="ห้องพัดลม รายวัน ")

    air_price_month = models.IntegerField(default=0,verbose_name="ห้องแอร์ รายเดือน ")
    air_price_day = models.IntegerField(default=0,verbose_name="ห้องแอร์ รายวัน ")
    electric_unit = models.IntegerField(default=0,verbose_name="อัตราค่าไฟฟ้า หน่วยละ ")
    water_unit = models.IntegerField(default=0,verbose_name="อัตราค่าน้ำประปา หน่วยละ ")
    water_month = models.IntegerField(default=0,verbose_name="อัตราค่าน้ำประปา คน/เดือน")
    water_internet = models.IntegerField(default=0,verbose_name="อัตราค่าบริการอินเตอร์เน็ตรายเดือน ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DormStyle(models.Model):
    class Meta:
        verbose_name = _("รายละเอียดหอพัก")
        verbose_name_plural = _("รายละเอียดหอพัก")
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    # choice = models.ManyToManyField(Choice) 
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE ,verbose_name="ตัวเลือก" )
    other = models.CharField(blank=True, null=True,max_length=100,verbose_name="อื่นๆ")

class DormImage(models.Model):
    class Meta:
        verbose_name = _("รูปภาพหอพัก")
        verbose_name_plural = _("รูปภาพหอพัก")
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    front = models.FileField(blank=True, null=True,upload_to='dorm/', verbose_name="รูปป้ายชื่อหน้าหอพัก")
    all_dorm = models.FileField(blank=True, null=True,upload_to='dorm/', verbose_name="รูปภาพมุมกว้างของหอพัก")
    front_room = models.FileField(blank=True, null=True,upload_to='dorm/', verbose_name="รูปภาพหน้าห้องพัก")
    in_room = models.FileField(blank=True, null=True,upload_to='dorm/', verbose_name="รูปภาพภายในห้องพัก")
    closet = models.FileField(blank=True, null=True,upload_to='dorm/', verbose_name="รูปภาพตู้เสื้อผ้า")
    bed = models.FileField(blank=True, null=True,upload_to='dorm/', verbose_name="รูปภาพเตียงนอน")
    wc = models.FileField(blank=True, null=True,upload_to='dorm/', verbose_name="รูปภาพห้องน้ำ")
    car = models.FileField(blank=True, null=True,upload_to='dorm/', verbose_name="รูปภาพลานจอดรถ")

class DormOwner(models.Model):
    class Meta:
        verbose_name = _("ผู้ประกอบการ")
        verbose_name_plural = _("ผู้ประกอบการ")
    OWNERS = (
        ('เจ้าของหอพักดูแลเอง','เจ้าของหอพักดูแลเอง'),
        ('แม่บ้าน / คนงานดูแล', 'แม่บ้าน / คนงานดูแล'), 
    )
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    name = models.CharField(blank=True, null=True,max_length=100,verbose_name="ชื่อ-สกุล")
    type_owner = models.CharField(blank=True, null=True,max_length=100,choices=OWNERS,verbose_name="ตำแหน่ง")

class About(models.Model):
    class Meta:
        verbose_name = _("ตั้งค่าหน้า เกี่ยวกับ")
        verbose_name_plural = _("ตั้งค่าหน้า เกี่ยวกับ")
    title = models.CharField(max_length=255,verbose_name="หัวข้อ")
    text = models.CharField(max_length=255,verbose_name="เนื้อหาย่อย")
    beta = models.BooleanField(default=True,verbose_name="อยู่ในช่วงพัฒนา")
    body = RichTextField(verbose_name="เนื้อหา")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}|{}'.format(self.title,self.text)