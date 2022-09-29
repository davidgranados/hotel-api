"""
Views for the hotel APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import HotelRoom, HotelRoomReservation, ReservationInvoiceDetails
from hotel import serializers


class HotelRoomViewSet(viewsets.ModelViewSet):
    """ViewSet for manage hotel room APIs."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.HotelRoomSerializer
    queryset = HotelRoom.objects.all()


class ReservationInvoiceDetailsViewSet(viewsets.ModelViewSet):
    """ViewSet for manage reservation invoice details APIs."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.ReservationInvoiceDetailsSerializer
    queryset = ReservationInvoiceDetails.objects.all()


class HotelRoomReservationViewset(viewsets.ModelViewSet):
    """ViewSet for manage hotel room reservation APIs."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.HotelRoomReservationSerializer
    queryset = HotelRoomReservation.objects.all()

    def perform_destroy(self, instance):
        """Delete the reservation."""
        instance.status = HotelRoomReservation.Status.CANCELLED
        instance.save()
