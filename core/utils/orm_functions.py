import os
import django


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from phpsupport.models import User, Order, Employee


def create_user(message):
    user, created_user = User.objects.get_or_create(chat_id=message.chat.id, username=message.chat.username)
    print(user, created_user)

def create_employee(message):
    user, created_user = Employee.objects.get_or_create(chat_id=message.chat.id, username=message.chat.username)
    print(user, created_user)

def create_client_order(message, description_order, order_date):
    user_id = User.objects.filter(chat_id=message['from'].id).first()

    created_order = Order.objects.create(user=user_id, description_order=description_order,
                                         order_date=order_date)
    return created_order

def get_client_orders(message):
    orders = Order.objects.filter(user__chat_id=message['from'].id)
    return orders

def get_all_new_orders():
    orders = Order.objects.filter(order_status='new')
    return orders


def upgrate_order_status(order_id, callback):
    order = Order.objects.filter(id=order_id).first()
    order.order_status = 'in_progress'
    employee_id = Employee.objects.filter(chat_id=callback.from_user.id).first()

    order.employee = employee_id
    order.save()
    return order