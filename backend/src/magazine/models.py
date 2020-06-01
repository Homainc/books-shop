from django.db import models
from sorl.thumbnail import ImageField
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.gis.db import models as models_gis
import datetime


class TypeProduct(models.Model):
    """ Type product: books, notepads and etc """
    type = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Тип продукта"
        verbose_name_plural = "Тип продуктов"

    def __str__(self):
        return self.type


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_time = models.DateField()
    count = models.IntegerField()
    type = models.ForeignKey(TypeProduct, on_delete=models.CASCADE)
    image = ImageField(upload_to='uploads')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f'{self.name}'

    def get_price(self):
        return self.price
    
    @property
    def get_count(self):
        return self.count
    
    @get_count.setter
    def set_count(self, new_count):
        self.count = new_count


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    product_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Продукт корзины"
        verbose_name_plural = "Продукты корзины"

    def __str__(self):
        return f'Объект корзины {self.product.name}'
    

class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartItem)
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
    
    def __str__(self):
        return f'Корзина пользователя {self.owner.username}'

    def add_to_cart(self, cart_item, owner):
        cart_item = CartItem.objects.get(id=cart_item.id)
        cart_owner = Cart.objects.get(owner=owner)
        if cart_item not in cart_owner.products.all():
            self.products.add(cart_item)
            self.save()

    def remove_from_cart(self, product, cart_item_id):
        for _item in self.products.all():
            if _item.product == product:
                self.products.remove(_item)
                product.count += _item.count
                product.save()
                self.cart_total -= _item.product_total
                self.save()
    
    def change_from_cart(self, count, cart_item):
        cart_item.count = int(count)
        cart_item.product_total = int(count) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in self.products.all():
            new_cart_total += float(item.product_total)
        self.cart_total = new_cart_total
        self.save()


ORDER_STATUS_CHOICES = [
    ("Принят к обработке", "Принят к обработке"),
    ("Выполняется", "Выполняется"),
    ("Оплачен", "Оплачен"),
]

ORDER_TYPE_OF_PURCHASE = [
    ("Доставка курьером", "Доставка курьером"),
    ("Самовывоз", "Самовывоз"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    busy = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username

    @property
    def get_busy(self):
        return self.busy

    @get_busy.setter
    def get_busy(self, state):
        self.busy = state


class Location(models.Model):
    title = models.CharField(max_length=80, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                blank=True, null=True)
    point = models_gis.PointField(default='POINT(0 0)', srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Геолокация"
        verbose_name_plural = "Геолокации"

    def __str__(self):
        return f'Aдрес: {self.title}'

    @property
    def longitude(self):
        return self.point[0]

    @property
    def latitude(self):
        return self.point[1]


class Shop(models.Model):
    name = models.CharField(max_length=50)
    personal = models.ManyToManyField(Profile)
    position = models.ForeignKey(Location, on_delete=models.CASCADE)
    starts_working = models.TimeField(default=datetime.time(hour=9, minute=0, second=0))
    finishes_working = models.TimeField(default=datetime.time(hour=22, minute=0, second=0))

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return f'Магазин {self.name}'

    @staticmethod
    def _working():
        time_now, _ = datetime.datetime.now(), datetime.datetime.today()
        time_close = datetime.datetime.combine(_,datetime.time(hour=22, minute=0, second=0))
        if time_now > time_close:
            return False
        return True


class RoomOrder(models.Model):
    """ In room exist client and courier,
    they can sharing location between themselves
    """
    participants = models.ManyToManyField(
        Profile, related_name='room', blank=True
    )
    locations = models.ManyToManyField(Location, blank=True)

    class Meta:
        verbose_name = "Комната клиент-курьер"
        verbose_name_plural = "Комнаты клиент-курьер"

    def __str__(self):
        return f"Комната {self.id}"


class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=13)
    date = models.DateTimeField(default=datetime.datetime.today)
    purchase_type = models.CharField(max_length=30, choices=ORDER_TYPE_OF_PURCHASE, default="Самовывоз")
    status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default="Принят к обработке")
    payment = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ номер {self.id}"

    @staticmethod
    def search_free_driver():
        profile_drivers = Profile.objects.filter(
            busy=False,
            user__is_staff=True
        ).first()
        return profile_drivers

    @property
    def check_status(self):
        return self.status

    @check_status.setter
    def check_status(self, new_status):
        self.status = new_status
        if self.status == "Оплачен":
            self.delete()
    

    


