from django.contrib import admin

from .models import User, Order, Employee

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    fields = ('chat_id', 'username')

@admin.register(Employee)
class AdminUser(admin.ModelAdmin):
    fields = ('chat_id', 'username')

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    fields = ('user', 'description_order', 'order_date', 'order_status', 'employee')