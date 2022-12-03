from django.urls import path
from BudgetTracker import views 

urlpatterns = [
    path('Input/delete/<input_id>', views.delete_input, name='delete_input'),
    path('Input/edit/<input_id>', views.edit_input, name='edit_input'),
]
