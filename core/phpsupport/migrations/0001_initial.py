# Generated by Django 3.2.4 on 2023-02-16 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='ID TG CHAT')),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description_order', models.TextField(blank=True, max_length=200, null=True, verbose_name='Описание заказа')),
                ('order_date', models.DateTimeField(verbose_name='Дата выполнения заказа')),
                ('order_status', models.CharField(blank=True, choices=[('new', 'Новый'), ('in_progress', 'В работе'), ('done', 'Выполнен')], default='new', max_length=200, null=True, verbose_name='Статус заказа')),
                ('performer', models.CharField(blank=True, max_length=200, null=True, verbose_name='Исполнитель')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_orders', to='phpsupport.user', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
