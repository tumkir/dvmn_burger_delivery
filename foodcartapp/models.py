from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class OrderQuerySet(models.QuerySet):

    def calculate_order_price(self):
        return self.annotate(price=Sum(F('items__price') * F('items__quantity')))


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50, db_index=True)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = models.CharField('контактный телефон', max_length=50, blank=True)

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name="ресторан"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт'
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


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
    phonenumber = PhoneNumberField(verbose_name='Телефон')
    address = models.CharField(max_length=500, verbose_name='Адрес')
    payment_method = models.CharField(max_length=5, choices=PAYMENT_METHOD_CHOICES, blank=True,
                                      db_index=True, verbose_name='Способ оплаты')
    status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default='NEW',
                              db_index=True, verbose_name='Статус заказа')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    registrated_at = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='Зарегистрирован в')
    called_at = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name='Позвонили в')
    delivered_at = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name='Доставлен в')

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.firstname} {self.lastname} {self.address}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], verbose_name='Количество')
    price = models.PositiveSmallIntegerField(verbose_name='Цена на момент создания заказа')

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def __str__(self):
        return f'{self.product} {self.order}'


class Place(models.Model):
    address = models.CharField(max_length=500, verbose_name='Адрес', unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота')
    request_to_geocoder_at = models.DateTimeField(default=timezone.now, db_index=True,
                                                  verbose_name='Координаты получены')

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return self.address
