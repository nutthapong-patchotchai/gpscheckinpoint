from django.contrib import admin
from .models import point, gps
from .models import point, gps  
from .models import Geography, Province  , Amphur ,District ,profile
from django.contrib.auth.models import User

admin.site.site_header = 'ระบบ อ.ว. การโควิด'

class profileAdmin(admin.ModelAdmin):
    search_fields = ['address']
    list_display = ('full_name','address', 'post','tel')
admin.site.register(profile,profileAdmin)
 
admin.site.register(gps)
admin.site.register(point) 



class GeographyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('id', 'name')
admin.site.register(Geography,GeographyAdmin)

class ProvinceAdmin(admin.ModelAdmin): 
    search_fields = ['name','code']
    list_display = ('id','code', 'name','geo') 
admin.site.register(Province,ProvinceAdmin) 

class AmphurAdmin(admin.ModelAdmin):
    search_fields = ['name','code']
    list_display = ('id','code', 'name','province','geo')
admin.site.register(Amphur,AmphurAdmin)  

class DistrictAdmin(admin.ModelAdmin):
    search_fields = ['name','code']
    list_display = ('id','code', 'name','amphur','province','geo')
admin.site.register(District,DistrictAdmin) 