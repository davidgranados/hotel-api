from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model that support using email instead of username.
    """

    username = None
    email = models.EmailField(_("email address"), max_length=255, unique=True, blank=False, null=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class HotelRoom(models.Model):
    """Hotel room object."""

    room_number = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.room_number


class ReservationInvoiceDetails(models.Model):
    """Reservation invoice details object."""

    class PaymentMethod(models.TextChoices):
        """Payment method choices."""

        CASH = "cash", _("Cash")
        CARD = "card", _("Card")

    reservation = models.OneToOneField(
        "HotelRoomReservation",
        on_delete=models.CASCADE,
        related_name="invoice",
    )
    invoice_date = models.DateField()
    invoice_number = models.CharField(max_length=255)

    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_method = models.CharField(
        max_length=4,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CARD,
    )

    def __str__(self):
        return f"Reservation: {self.reservation.id} - Room: {self.hotel_room.room_number}"


class ReservationGuestDetails(models.Model):
    """Reservation guest details object."""

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    is_main = models.BooleanField(default=False)
    reservation = models.ForeignKey(
        "HotelRoomReservation",
        on_delete=models.CASCADE,
        related_name="guests",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class HotelRoomReservation(models.Model):
    """Hotel room reservation object."""

    class Status(models.TextChoices):
        """Reservation status."""

        PENDING = "pending", _("Pending")
        CONFIRMED = "paid", _("Paid")
        CANCELLED = "cancelled", _("Cancelled")

    room = models.ForeignKey(
        "HotelRoom",
        on_delete=models.PROTECT,
    )
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(
        max_length=255,
        choices=Status.choices,
        default=Status.PENDING,
    )

    class Meta:
        unique_together = ("room", "check_in_date", "check_out_date")

    def __str__(self):
        return f"{self.room.room_number} - {self.status}"
