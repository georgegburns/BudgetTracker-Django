from .models import *
from django import forms
import django_filters as df

class spendfilter(df.FilterSet):
    cost_centre__cost_centre = df.AllValuesFilter(empty_label='All', label='Cost Centre')
    nominal__nominal = df.AllValuesFilter(empty_label='All', label='Nominal')
    supplier__supplier = df.AllValuesFilter(empty_label='All', label='Supplier')
    start_date_filter = df.DateFilter(field_name='date', lookup_expr='gt', label='Date From')
    start_date_filter.field.widget = forms.DateInput(attrs={'type' : 'date'})
    end_date_filter = df.DateFilter(field_name='date', lookup_expr='lt', label='Date To')
    end_date_filter.field.widget = forms.DateInput(attrs={'type' : 'date'})
    from_spend_filter = df.NumberFilter(field_name='spend', label='£ From', lookup_expr='gt')
    from_spend_filter.field.widget = forms.NumberInput(attrs={'type' : 'number'})
    to_spend_filter = df.NumberFilter(field_name='spend', label='£ To', lookup_expr='lt')
    to_spend_filter.field.widget = forms.NumberInput(attrs={'type' : 'number'})
    spend_type__spend_type = df.AllValuesFilter(empty_label='All', label='Spend Type')
    description_filter = df.CharFilter(field_name='description', label='Description Contains', lookup_expr='icontains')
    class Meta:
        model = BudgetInput
        fields = ['cost_centre', 'nominal', 'supplier', 'spend', 'date', 'description']