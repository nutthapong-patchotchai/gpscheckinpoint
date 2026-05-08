from django_filters import CharFilter, Filter, FilterSet, NumberFilter
from dormitory.models import Choice, Dorm, DormStyle


def split_values(value):
    if not value:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(',') if item.strip()]
    return value

#ค้นหาแบบหลายค่าพร้อมๆกัน โดยใช้ , ครั้นไว้
class ListFilter(Filter):
    def filter(self, qs, value):
        values = split_values(value)
        if not values:
            return qs

        return qs.filter(**{f'{self.field_name}__in': values})

#ค้นหาแบบหลายค่าพร้อมๆกัน โดยใช้ , ครั้นไว้ และ ค้นหาแบบหลายtableพร้อมๆกัน โดยใช้ & ครั้นไว้ ใช้กับ Choice
class ChoiceFilter(FilterSet):
    name = ListFilter(field_name='name')
    value = ListFilter(field_name='value')

    class Meta:
        model = Choice
        fields = ['name', 'value']
        
#ค้นหาแบบหลายค่าพร้อมๆกัน โดยใช้ , ครั้นไว้ และ ค้นหาแบบหลายtableพร้อมๆกัน โดยใช้ & ครั้นไว้ ใช้กับ DormStyle
class DormStyleFilter(FilterSet):
    name = ListFilter(field_name='dorm')
    value = ListFilter(field_name='choice__value')

    class Meta:
        model = DormStyle
        fields = ['dorm', 'choice__value']
        
class BookFilterSet(FilterSet):
    id  = ListFilter(field_name='id') 
    zone = Filter(method='filter_zone')

    class Meta:
        model = Dorm
        fields = ['id','zone']

    def filter_zone(self, queryset, name, value):
        values = split_values(value)
        if not values:
            return queryset
        dorm_ids = DormStyle.objects.filter(
            choice__name="โซนหอพัก",
            choice__value__in=values,
        ).values_list('dorm_id', flat=True)
        return queryset.filter(id__in=dorm_ids)

#อันใหม่วันที่ 22/09/2020
class ZoneFilter(FilterSet):
    id = NumberFilter(field_name='id')
    zone = CharFilter(method='filter_zone')

    class Meta:
        model = Dorm
        fields = ['zone','id']

    def filter_zone(self, queryset, name, value):
        values = split_values(value)
        if not values:
            return queryset
        dorm_ids = DormStyle.objects.filter(
            choice__name="โซนหอพัก",
            choice__value__in=values,
        ).values_list('dorm_id', flat=True)
        return queryset.filter(id__in=dorm_ids)
