from django.db.models import Q
from django_filters import Filter, FilterSet
from dormitory.models import (Choice, Dorm, DormDetail, DormStyle, DormImage, DormOwner ,About)
from django_property_filter import PropertyFilterSet, PropertyNumberFilter,RangeFilter,PropertyBaseFilter,PropertyLookupChoiceFilter, PropertyCharFilter,PropertyAllValuesFilter,PropertyBaseInFilter,PropertyChoiceFilter

#ค้นหาแบบหลายค่าพร้อมๆกัน โดยใช้ , ครั้นไว้
class ListFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'in'
        values = value.split(',')
        return super(ListFilter, self).filter(qs, values)

#ค้นหาแบบหลายค่าพร้อมๆกัน โดยใช้ , ครั้นไว้ และ ค้นหาแบบหลายtableพร้อมๆกัน โดยใช้ & ครั้นไว้ ใช้กับ Choice
class ChoiceFilter(FilterSet):
    name = ListFilter(field_name='name')
    value = ListFilter(field_name='value')

    class Meta:
        model = Choice
        fields = ['name', 'value']
        
    def filter_both(self, queryset, name, value):
        return queryset.filter(
            Q(name=value) | Q(value=value)
        )
        
#ค้นหาแบบหลายค่าพร้อมๆกัน โดยใช้ , ครั้นไว้ และ ค้นหาแบบหลายtableพร้อมๆกัน โดยใช้ & ครั้นไว้ ใช้กับ DormStyle
class DormStyleFilter(FilterSet):
    name = ListFilter(field_name='dorm')
    value = ListFilter(field_name='choice__value')

    class Meta:
        model = DormStyle
        fields = ['dorm', 'choice__value']
        
    def filter_both(self, queryset, name, value):
        return queryset.filter(
            Q(name=value) | Q(value=value)
        )


class ListFilterProperty(PropertyBaseInFilter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'in'
        values = value.split(',')
        return super(ListFilterProperty, self).filter(qs, values)

class ListFilterArrProperty(PropertyBaseInFilter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'in'
        values = value.split(',')
        return super(ListFilterArrProperty, self).filter(qs, values)

class BookFilterSet(PropertyFilterSet):
    id  = ListFilter(field_name='id') 
    zone = ListFilterProperty(field_name='zone')
    class Meta:
        model = Dorm
        fields = ['id','zone']
        
    def filter_both(self, queryset, zone, id):
        return queryset.filter(
            Q(zone=id) | Q(id=zone)
        )