from django.contrib import admin
from .models import CibilPrediction, Bank

@admin.register(CibilPrediction)
class CibilPredictionAdmin(admin.ModelAdmin):
    list_display = ['predicted_score', 'age', 'monthly_income', 'desired_loan_amount', 'existing_loans', 'created_at']
    list_filter = ['predicted_score', 'created_at', 'existing_loans']
    search_fields = ['predicted_score']
    ordering = ['-created_at']

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'min_cibil_score', 'interest_rate', 'max_loan_amount']
    list_filter = ['min_cibil_score', 'interest_rate']