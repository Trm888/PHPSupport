from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import User, Order, Employee


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'subscription')


@admin.register(Employee)
class AdminUser(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'subscription')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'description_order', 'order_date', 'order_status', 'employee')
    actions = ['make_published']

    @admin.action(description='Mark selected order status as new')
    def make_published(self, request, queryset):
        updated = queryset.update(order_status='new')
        queryset.update(employee_id='')
        self.message_user(request, ngettext(
            '%d order was successfully marked as new.',
            '%d orders were successfully marked as new.',
            updated,
        ) % updated, messages.SUCCESS)