from django.contrib import admin
from .models import CovidCase, CoinTransaction, CoinWallet, cut_coin, gps, point, user_cut_coin
from .models import Geography, Province, Amphur ,District, profile 
from django.contrib.auth.models import User

admin.site.site_header = 'ระบบ อ.ว. การโควิด'

class user_cut_coinAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user','cut_coin']
    search_fields = ['user__username','user__first_name','user__last_name','cut_coin__title']
    list_display = ('full_name','coin','coin_score','coin_spent','activity_hours','balance_after','status','created_at','updated_at') 
    list_filter = ('cut_coin','status')
admin.site.register(user_cut_coin,user_cut_coinAdmin)


class cut_coinAdmin(admin.ModelAdmin):
    search_fields = ['title','coin','status']
    list_display = ('title','coin','activity_hours','etc','status','created_at','updated_at')
    list_filter = ('status',)
admin.site.register(cut_coin,cut_coinAdmin)


class CoinWalletAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    search_fields = ['user__username','user__first_name','user__last_name','user__email']
    list_display = ('owner_name','balance','current_streak','longest_streak','total_earned','total_spent','activity_hours','last_checkin_date','updated_at')
admin.site.register(CoinWallet,CoinWalletAdmin)


class CoinTransactionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user','wallet','checkin','redemption']
    search_fields = ['user__username','user__first_name','user__last_name','note']
    list_display = ('user','transaction_type','amount','balance_after','streak_day','note','created_at')
    list_filter = ('transaction_type','created_at')
admin.site.register(CoinTransaction,CoinTransactionAdmin)


class CovidCaseAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user','created_by']
    search_fields = ['user__username','user__first_name','user__last_name','user__email','notes']
    list_display = ('owner_name','status','symptom_started_on','confirmed_on','trace_start_date','trace_end_date','created_by','updated_at')
    list_filter = ('status','confirmed_on','created_at')
    readonly_fields = ('created_at','updated_at')
admin.site.register(CovidCase,CovidCaseAdmin)

class profileAdmin(admin.ModelAdmin):
    search_fields = ['address', 'faculty', 'user__first_name', 'user__last_name', 'user__username']
    list_display = ('full_name','faculty','address','province_name','amphur_name','district_name', 'post','tel')
admin.site.register(profile,profileAdmin)
 
class CheckinAdmin(admin.ModelAdmin):
    autocomplete_fields = ['province','amphur','district']
    search_fields = ['user__first_name','user__last_name','place_name','province__name','amphur__name','district__name','geo__name','created_at']
    list_display = ('id', 'full_name','place_name','geo_name','province_name','amphur_name','district_name','coins_awarded','streak_day','coin_awarded','created_at') 
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
