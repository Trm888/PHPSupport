import os
import django


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from phpsupport.models import User, Order

def get_client_order(message, description_order, order_date):
    user_id = User.objects.filter(chat_id=message['from'].id).first()

    created_order = Order.objects.create(user=user_id, description_order=description_order,
                                         order_date=order_date)
    return created_order