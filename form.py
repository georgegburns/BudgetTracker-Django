from django import forms
from .models import *
from django.conf import settings

class BudgetForm(forms.ModelForm):
    class Meta:
        date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
        model = BudgetInput
        fields = ['cost_centre', 'nominal', 'supplier', 'date', 'spend', 'spend_type', 'description']

class BudgetUploadForm(forms.ModelForm):
    class Meta:
        model = BudgetUpload
        fields = ['file_name',]
        
class ValueUploadForm(forms.ModelForm):
    class Meta:
        model = ValueUpload
        fields = ['file_name',]
        
class CCForm(forms.ModelForm):
    cost_centre = forms.CharField(label='New Cost Centre', required=False)
    class Meta:
        model = CC_Choices
        fields = ['cost_centre']
        
class NomForm(forms.ModelForm):
    nominal = forms.CharField(label='New Nominal', required=False)
    class Meta:
        model = Nom_Choices
        fields = ['nominal']
        
class SupForm(forms.ModelForm):
    supplier = forms.CharField(label='New Supplier', required=False)
    class Meta:
        model = Sup_Choices
        fields = ['supplier']
        
class STForm(forms.ModelForm):
    spend_type = forms.CharField(label="New Spend Type", required=False)
    class Meta:
        model = ST_Choices
        fields = ['spend_type']
        
        

    
    