from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'phone_number', 'customer_since')
    search_fields = ('user__username', 'user__email', 'account_number', 'phone_number')
    list_filter = ('customer_since',)
