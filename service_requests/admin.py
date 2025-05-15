from django.contrib import admin
from .models import ServiceRequest, ServiceRequestType, ServiceRequestAttachment

@admin.register(ServiceRequestType)
class ServiceRequestTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ServiceRequestAttachmentInline(admin.TabularInline):
    model = ServiceRequestAttachment
    extra = 0

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'status', 'created_at', 'updated_at', 'resolved_at')
    list_filter = ('status', 'request_type', 'created_at', 'resolved_at')
    search_fields = ('title', 'description', 'customer__user__username', 'customer__account_number')
    inlines = [ServiceRequestAttachmentInline]

@admin.register(ServiceRequestAttachment)
class ServiceRequestAttachmentAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'uploaded_at')
    list_filter = ('uploaded_at',)
