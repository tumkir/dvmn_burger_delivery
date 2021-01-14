from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField('контактный телефон', max_length=50, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                 verbose_name='категория', related_name='products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2)
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False, db_index=True)
    description = models.TextField('описание', max_length=200, blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='menu_items')
    availability = models.BooleanField('в продаже', default=True, db_index=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]


class Order(models.Model):

    ORDER_STATUS_CHOICES = [
        ('NEW', 'Необработанный'),
        ('COMPLETED', 'Обработанный')
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Наличными'),
        ('CARD', 'Электронно')
    ]

    firstname = models.CharField(max_length=200, verbose_name='Имя')
    lastname = models.CharField(max_length=200, verbose_name='Фамилия')
    phonenumber = models.CharField(max_length=40, verbose_name='Телефон')
    address = models.CharField(max_length=500, verbose_name='Адрес')
    payment_method = models.CharField(max_length=5, choices=PAYMENT_METHOD_CHOICES, blank=True)
    status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='NEW', verbose_name='Статус заказа')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    registrated_at = models.DateTimeField(default=timezone.now, verbose_name='Зарегистрирован в')
    called_at = models.DateTimeField(null=True, blank=True, verbose_name='Позвонили в')
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name='Доставлен в')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.address}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество')
    price = models.PositiveSmallIntegerField(verbose_name='Стоимость продукта')

    def __str__(self):
        return f'{self.product} {self.order}'

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
