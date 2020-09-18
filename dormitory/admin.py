from django.contrib import admin
from dormitory.models import  *
from django.contrib.admin import SimpleListFilter


# from dormitory.models import Zonedorm,Dormitory,Makefood,Sizedorm,Typedorm,Pet,Pricedorm

# admin.site.register(Zonedorm)
# admin.site.register(Dormitory)
# admin.site.register(Makefood)
# admin.site.register(Sizedorm)
# admin.site.register(Typedorm)
# admin.site.register(Pet)
# admin.site.register(Pricedorm)


class ChoiceAdmin(admin.ModelAdmin):  
    search_fields = ['name','value','id',]
    list_display = ('id','name','value',)
    list_filter = ('name',)

 
admin.site.register(Choice,ChoiceAdmin)
 
# admin.site.register(DormStyle)
# admin.site.register(Dorm)
# class DormdminModel(admin.ModelAdmin):
#     list_filter = ('dorm',)
#     filter_horizontal = ('choice',)

# admin.site.register(DormStyle,DormdminModel)
class DormOwnerInline(admin.TabularInline):
    model = DormOwner
    # filter_horizontal = ('choice',)
    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra
class WoodInline(admin.TabularInline):
    model = DormStyle
    # filter_horizontal = ('choice',)
    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra
class DormDetailInline(admin.TabularInline):
    model = DormDetail
    # filter_horizontal = ('choice',)
    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra
class DormImageInline(admin.TabularInline):
    model = DormImage
    # filter_horizontal = ('choice',)
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
            # data = Choice.objects.filter(name="โซนหอพัก").filter(value=self.value()).values_list('id', flat=True)
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