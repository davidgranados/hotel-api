"""
URL mappings fot the hotel app.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from hotel import views

router = DefaultRouter()
router.register("rooms", views.HotelRoomViewSet)
router.register("invoices", views.ReservationInvoiceDetailsViewSet)
router.register("reservations", views.HotelRoomReservationViewset)

app_name = "hotel"

urlpatterns = [
    path("", include(router.urls)),
]
