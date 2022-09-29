from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from core.models import (
    CustomUser,
    HotelRoom,
    HotelRoomReservation,
    ReservationGuestDetails,
    ReservationInvoiceDetails,
)

admin.site.register(HotelRoom)
admin.site.register(ReservationInvoiceDetails)
admin.site.register(HotelRoomReservation)
admin.site.register(ReservationGuestDetails)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ["id"]
    list_display = ["email", "first_name", "last_name"]
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_active", "is_staff", "is_superuser"),
            },
        ),
    )
