from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.

class CC_Choices(models.Model):
    cost_centre = models.CharField(("cost_centre"),max_length=6)
    
    def __str__(self):
        return self.cost_centre
    
    class Meta:
        unique_together = [['cost_centre',]]
    
class Nom_Choices(models.Model):
    nominal = models.CharField(("nominal"),max_length=50)
    
    def __str__(self):
        return self.nominal
    
    class Meta:
        unique_together = [['nominal',]]

class Sup_Choices(models.Model):
    supplier = models.CharField(("supplier"),max_length=20, blank=True)
    
    def __str__(self):
        return self.supplier
    
    class Meta:
        unique_together = [['supplier',]]
    
class ST_Choices(models.Model):
    spend_type = models.CharField(("spend_type"),max_length=2)
    
    def __str__(self):
        return self.spend_type
    
    class Meta:
        unique_together = [['spend_type',]]

class BudgetInput(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    cost_centre = models.ForeignKey(CC_Choices, on_delete=models.CASCADE)
    nominal = models.ForeignKey(Nom_Choices, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Sup_Choices, on_delete=models.CASCADE)
    date = models.DateField(("date"), blank=True)
    spend = models.FloatField(("spend"),max_length=5, blank=True)
    spend_type = models.ForeignKey(ST_Choices, on_delete=models.CASCADE)
    description = models.CharField(("description"),max_length=100, blank=True)
    
    class Meta:
        unique_together = [['cost_centre', 'nominal', 'supplier', 'date', 'spend', 'spend_type']]
    
class BudgetUpload(models.Model):
    file_name = models.FileField((""),upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"File id: {self.id}"
    
class ValueUpload(models.Model):
    file_name = models.FileField((""),upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"File id: {self.id}"