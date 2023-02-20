from django.contrib import admin

from .models import User, Order, Employee


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'subscription')


@admin.register(Employee)
class AdminUser(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'subscription')


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('user', 'description_order', 'order_date', 'order_status', 'employee')
