from django.contrib import admin
from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'transaction_type',
        'category',
        'amount',
        'date'
    ]

    list_filter = [
        'transaction_type',
        'category',
        'date'
    ]

    search_fields = [
        'description'
    ]