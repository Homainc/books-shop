# Generated by Django 3.0.3 on 2020-07-02 15:45

import datetime
from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('point', django.contrib.gis.db.models.fields.PointField(default='POINT(0 0)', srid=4326)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Геолокация',
                'verbose_name_plural': 'Геолокации',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('busy', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='TypeProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Тип продукта',
                'verbose_name_plural': 'Тип продуктов',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('starts_working', models.TimeField(default=datetime.time(9, 0))),
                ('finishes_working', models.TimeField(default=datetime.time(22, 0))),
                ('personal', models.ManyToManyField(to='magazine.Profile')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.Location')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='RoomOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locations', models.ManyToManyField(blank=True, to='magazine.Location')),
                ('participants', models.ManyToManyField(blank=True, related_name='room', to='magazine.Profile')),
            ],
            options={
                'verbose_name': 'Комната клиент-курьер',
                'verbose_name_plural': 'Комнаты клиент-курьер',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('delivery_time', models.DateField()),
                ('count', models.IntegerField()),
                ('image', sorl.thumbnail.fields.ImageField(default='uploads/default.png', upload_to='uploads')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.TypeProduct')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=13)),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 7, 2, 15, 45, 4, 514586))),
                ('purchase_type', models.CharField(choices=[('Доставка курьером', 'Доставка курьером'), ('Самовывоз', 'Самовывоз')], default='Самовывоз', max_length=30)),
                ('status', models.CharField(choices=[('Принят к обработке', 'Принят к обработке'), ('Выполняется', 'Выполняется'), ('Оплачен', 'Оплачен')], default='Принят к обработке', max_length=30)),
                ('payment', models.BooleanField(default=False)),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.Cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.Profile')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.AddField(
            model_name='location',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.Profile'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1)),
                ('product_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.Product')),
            ],
            options={
                'verbose_name': 'Продукт корзины',
                'verbose_name_plural': 'Продукты корзины',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magazine.Profile'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(to='magazine.CartItem'),
        ),
    ]
