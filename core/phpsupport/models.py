from django.db import models


class User(models.Model):
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    chat_id = models.CharField(
        verbose_name='ID TG CHAT',
        max_length=10,
        blank=True,
        null=True)
    username = models.CharField(
        max_length=200,
        blank=True,
        null=True)
    def __str__(self):
        return f'{self.username}'

class Employee(models.Model):
    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    chat_id = models.CharField(
        verbose_name='ID TG CHAT',
        max_length=10,
        blank=True,
        null=True)
    username = models.CharField(
        max_length=200,
        blank=True,
        null=True)
    def __str__(self):
        return f'{self.username}'

class Order(models.Model):

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    user = models.ForeignKey(
        User,
        related_name='user_orders',
        verbose_name='Клиент',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    description_order = models.TextField(
        verbose_name='Описание заказа',
        max_length=200, blank=True, null=True)

    order_date = models.DateField(
        verbose_name='Дата выполнения заказа',
    )

    order_status = models.CharField(
        verbose_name='Статус заказа',
        choices=(
            ('new', 'Новый'),
            ('in_progress', 'В работе'),
            ('done', 'Выполнен'),
        ),
        max_length=200, blank=True, null=True, default='new'
    )

    employee = models.ForeignKey(
        Employee,
        related_name='employee_orders',
        verbose_name='Исполнитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user} - {self.description_order} - {self.order_date} - {self.order_status} - {self.employee}'