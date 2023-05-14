from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import qrcode

# Create your models here.


class CustomUser(AbstractUser):
    user_type_choices = ((1, "Admin"),(2, "Staff"))
    user_type = models.CharField(max_length=255, choices=user_type_choices, default=1)


class AdminUser(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auth_user_id.username}- {self.auth_user_id.user_type}"


class StaffUser(models.Model):
    profile_pic = models.FileField(default="")
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auth_user_id.username}- {self.auth_user_id.user_type}"


# STATUS
class OrdenesRate(models.IntegerChoices):
    ORDEN_RATE_1 = 1, _("Anulada")
    ORDEN_RATE_2 = 2, _("Coordinado Con Proveedores")
    ORDEN_RATE_3 = 3, _("Cliente No Responde")
    ORDEN_RATE_4 = 4, _("Proceso de Activacion")
    ORDEN_RATE_5 = 5, _("Proceso Finalizado")


class StatusOrderProveedor(models.IntegerChoices):
    STATUS_RATE_1 = 1, _("Anulada")
    STATUS_RATE_2 = 2, _("Coordinado Con Proveedores")
    STATUS_RATE_3 = 3, _("Proveedor No Responde")
    STATUS_RATE_4 = 4, _("Proceso de Activacion")
    STATUS_RATE_5 = 5, _("Proceso Finalizado")


class PayModels(models.IntegerChoices):
    Efectivo_Dolar = 1, _("Dolares Efectivo")
    Efectivo_Local = 2, _("Moneda Local")
    Digital = 3, _("Moneda o Tokens Digitales")
    Otros = 4, _("Otras Wallets")


class Range(models.IntegerChoices):
    RATING_1 = 1, _("Cliente Con Deuda")
    RATING_2 = 2, _("Cliente Desiste")
    RATING_3 = 3, _("Cliente Sin Oferta")
    RATING_4 = 4, _("Cliente Vigente")


class Proveedor(models.Model):
    auth_user_id = models.AutoField(primary_key=True)
    profile_pic = models.FileField(default="")
    company_name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField(verbose_name=_("Email del Proveedor"), max_length=50)
    phone_number = models.CharField(
        verbose_name=_("Numero del Provedor"), max_length=50
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # objects = models.Manager()

    def __str__(self):
        return f"{self.auth_user_id} -{self.company_name} -{self.email} -{self.phone_number}"


class Categorie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("category_list")

    def __str__(self):
        return f"{self.id}- {self.title}- {self.description}- {self.created_at}- {self.is_active}"


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    categories_id = models.ForeignKey(
        Categorie, on_delete=models.CASCADE, blank=True, null=True
    )
    product_name = models.CharField(max_length=255)
    price = models.CharField(max_length=7)
    product_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name}- {self.categories_id.title}- {self.price}"


class ProductMedia(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True
    )
    media_type_choice = ((1, "Image"), (2, "Video"))
    media_type = models.CharField(max_length=255)
    media_content = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.IntegerField(default=1)


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.ForeignKey(
        Products, on_delete=models.CASCADE, blank=True, null=True
    )
    cantidad_stock = models.IntegerField(
        verbose_name=_("Cantidad del Stock"), default=0
    )
    descripcion = models.CharField(max_length=255)
    precio = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.products.id}- {self.products.categories_id.title}- {self.products.product_name}- {self.cantidad_stock}- {self.precio}"


class OrderStock(models.Model):
    id = models.AutoField(primary_key=True)
    Proveedor_id = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, blank=True, null=True
    )
    product_id = models.ForeignKey(
        Stock, on_delete=models.CASCADE, blank=True, null=True
    )
    cantidad = models.IntegerField(verbose_name=_("Cantidad"), default=0)
    price = models.IntegerField(verbose_name=_("Precio"), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        verbose_name=_("Rating del Stock-Proveedor"),
        choices=StatusOrderProveedor.choices,
        default="En Proceso",
    )

    def update_products_stock(self):
        if self.rating == StatusOrderProveedor.STATUS_RATE_5:
            stock = OrderStock.objects.filter(product_id=Stock)
            stock.cantidad_stock += self.cantidad
            stock.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_products_stock()


class Cliente(models.Model):
    dni = models.CharField(max_length=50, blank=False, null=False)
    nombres = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(verbose_name=_("Email del Cliente"), max_length=50)
    celular = models.CharField(verbose_name=_("Numero del Cliente"), max_length=50)
    pais = models.CharField(max_length=50, default="Usa")
    ciudad = models.CharField(max_length=180, default="Miami", blank=False, null=False)
    direccion = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f"{self.dni}- {self.nombres}- {self.apellidos}- {self.celular}"


class ClienteStatus(models.Model):
    cliente_id = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True
    )
    rating = models.IntegerField(
        verbose_name=_("Rating del Cliente"),
        choices=Range.choices,
        default="En Proceso",
    )


class Order(models.Model):
    transaction_id =  models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.activo == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.Stock.precio * self.quantity
        return total


class Payments(models.Model):
    id = models.AutoField(primary_key=True)
    orderitem = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    payments = models.IntegerField(
        verbose_name=_("Metodo de Pago"),
        choices=PayModels.choices,
        default="Dolares $",
    )
    status = models.BooleanField(default=False, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

##### DELIVERY

class OrderDeliveryStatus(models.Model):
    qr_code = models.ImageField(
        upload_to="qrcodes/", blank=True, null=True, editable=False
    )
    order_id = models.ForeignKey(Payments, on_delete=models.CASCADE)
    status = models.IntegerField(
        verbose_name=_("Rating del Servicio"),
        choices=OrdenesRate.choices,
    )
    status_message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(OrderDeliveryStatus, self).save(*args, **kwargs)

        # Generar el código QR y guardarlo como una imagen en el campo qr_code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"media/qrcodes/{self.id}.png")
        self.qr_code = f"qrcodes/{self.id}.png"
        super(OrderDeliveryStatus, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminUser.objects.create(auth_user_id=instance)
        if instance.user_type == 2:
            StaffUser.objects.create(auth_user_id=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminuser.save()
    if instance.user_type == 2:
        instance.staffuser.save()


# Se define una señal que se activará cada vez que se guarde con un Proveedor un objeto OrderStock
@receiver(post_save, sender=OrderStock)
def update_stock_Proveedor(sender, instance, **kwargs):
    # Se verifica si el rating del OrderStock es igual a STATUS_RATE_5
    if instance.rating == StatusOrderProveedor.STATUS_RATE_5:
        # Se actualiza la cantidad de productos en el Stock correspondiente
        stock = Stock.objects.get(products=instance.id)
        stock.cantidad_stock += instance.cantidad
        stock.save()
        # Se muestra una lista con los productos actualizados
        update_stock = Stock.objects.all()
        for producto in update_stock:
            print(f"{producto.products}: {producto.cantidad_stock}")


# Se define una señal que se activará cada vez que se guarde un objeto en la tabla OrderStock
@receiver(post_save, sender=OrderStock)
def update_stock(sender, instance, **kwargs):
    # Se verifica si el rating del OrderStock es igual a STATUS_RATE_5
    if instance.rating == StatusOrderProveedor.STATUS_RATE_5:
        # Se actualiza la cantidad de productos en el Stock correspondiente
        stock = Stock.objects.get(products=instance.product_id)
        stock.cantidad_stock += instance.cantidad
        stock.save()
        # Se muestra una lista con los productos actualizados
        update_stock = Stock.objects.all()
        for producto in update_stock:
            print(f"{producto.products}: {producto.cantidad_stock}")


@receiver(post_save, sender=Payments)
def create_order_delivery_status(sender, instance, created, **kwargs):
    if instance.status:
        order_delivery_status = OrderDeliveryStatus(order_id=instance)
        order_delivery_status.save()
