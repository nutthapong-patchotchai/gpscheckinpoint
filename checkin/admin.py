from django.contrib import admin
from .models import point, gps
from .models import point, gps, cut_coin,user_cut_coin
from .models import Geography, Province, Amphur ,District, profile 
from django.contrib.auth.models import User

admin.site.site_header = 'ระบบ อ.ว. การโควิด'

class user_cut_coinAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user','cut_coin']
    search_fields = ['coin','full_name','cut_coin']
    list_display = ('full_name','coin','coin_score','created_at','updated_at') 
    list_filter = ('cut_coin',)
admin.site.register(user_cut_coin,user_cut_coinAdmin)


class cut_coinAdmin(admin.ModelAdmin):
    search_fields = ['title','coin','status']
    list_display = ('title','coin','etc','status','created_at','updated_at')
    list_filter = ('status',)
admin.site.register(cut_coin,cut_coinAdmin)

class profileAdmin(admin.ModelAdmin):
    search_fields = ['address']
    list_display = ('full_name','address','province_name','amphur_name','district_name', 'post','tel')
admin.site.register(profile,profileAdmin)
 
class CheckinAdmin(admin.ModelAdmin):
    autocomplete_fields = ['province','amphur','district']
    search_fields = ['user__first_name','user__last_name','province__name','amphur__name','district__name','geo__name','created_at']
    list_display = ('id', 'full_name','geo_name','province_name','amphur_name','district_name','created_at') 
admin.site.register(gps,CheckinAdmin)

class pointAdmin(admin.ModelAdmin): 
    search_fields = ['user__first_name','user__last_name']
    list_display = ('full_name','created_at','updated_at')
admin.site.register(point,pointAdmin) 
 
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