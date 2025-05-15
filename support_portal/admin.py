from django.contrib import admin
from .models import SupportStaff, ServiceRequestNote

@admin.register(SupportStaff)
class SupportStaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_id', 'department')
    search_fields = ('user__username', 'user__email', 'staff_id')
    list_filter = ('department',)

@admin.register(ServiceRequestNote)
class ServiceRequestNoteAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'staff', 'created_at', 'internal_only')
    list_filter = ('internal_only', 'created_at')
    search_fields = ('content', 'staff__user__username', 'service_request__title')
