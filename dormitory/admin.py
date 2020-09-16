from django.contrib import admin
from dormitory.models import  *
# from dormitory.models import Zonedorm,Dormitory,Makefood,Sizedorm,Typedorm,Pet,Pricedorm

# admin.site.register(Zonedorm)
# admin.site.register(Dormitory)
# admin.site.register(Makefood)
# admin.site.register(Sizedorm)
# admin.site.register(Typedorm)
# admin.site.register(Pet)
# admin.site.register(Pricedorm)




 
admin.site.register(Choice)

admin.site.register(DormStyle)
# admin.site.register(Dorm)
# class DormdminModel(admin.ModelAdmin):
#     list_filter = ('dorm',)
#     filter_horizontal = ('choice',)

# admin.site.register(DormStyle,DormdminModel)

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
class PropertiesAdmin(admin.ModelAdmin): 
    inlines = [DormDetailInline,WoodInline,DormImageInline, ] 
    autocomplete_fields = ['province','amphur','district']

admin.site.register(Dorm, PropertiesAdmin)

admin.site.register(About)