from django.contrib import admin
from dormitory.models import (
    About,
    Choice,
    Dorm,
    DormDetail,
    DormImage,
    DormOwner,
    DormStyle,
    UserDorm,
)

class UserDormAdmin(admin.ModelAdmin):  
    search_fields = ['full_name','dorm__id','id',]
    list_display = ('full_name','dorm_name','created_at')
    list_filter = ('dorm__name',)


 
admin.site.register(UserDorm,UserDormAdmin)

class ChoiceAdmin(admin.ModelAdmin):  
    search_fields = ['name','value','id',]
    list_display = ('id','name','value',)
    list_filter = ('name',)

 
admin.site.register(Choice,ChoiceAdmin)
 
class DormOwnerInline(admin.TabularInline):
    model = DormOwner

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra
class WoodInline(admin.TabularInline):
    model = DormStyle

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra
class DormDetailInline(admin.TabularInline):
    model = DormDetail

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra
class DormImageInline(admin.TabularInline):
    model = DormImage

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra

class IsLiveFilter(admin.SimpleListFilter):
    title = 'โซน'
    parameter_name = 'ss'
    def lookups(self, request, model_admin):
        return (
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
            ('E', 'E')
    )
    def queryset(self, request, queryset):
        if self.value(): 
            get = DormStyle.objects.filter(choice__value=self.value()).values_list('dorm_id', flat=True)
            return queryset.filter(pk__in=get)

class PropertiesAdmin(admin.ModelAdmin): 
    inlines = [DormOwnerInline,DormDetailInline,WoodInline,DormImageInline, ] 
    autocomplete_fields = ['province','amphur','district']  
    search_fields = ['name','address','id']
    list_display = ('id','name','address','permission','advt','zone')
    list_filter = ('permission','advt',IsLiveFilter)

admin.site.register(Dorm, PropertiesAdmin)

admin.site.register(About)

admin.site.register(DormStyle)
