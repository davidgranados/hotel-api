"""
Serializers fro hotel APIs
"""
from rest_framework import serializers

from core.models import (
    HotelRoom,
    HotelRoomReservation,
    ReservationGuestDetails,
    ReservationInvoiceDetails,
)


class HotelRoomSerializer(serializers.ModelSerializer):
    """Serializer for hotel room objects."""

    class Meta:
        model = HotelRoom
        fields = ["id", "room_number"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a new hotel room."""
        return HotelRoom.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a hotel room."""
        instance.room_number = validated_data.get("room_number", instance.room_number)
        instance.save()
        return instance


class ReservationGuestDetailsSerializer(serializers.ModelSerializer):
    """Serializer for reservation guest details objects."""

    class Meta:
        model = ReservationGuestDetails
        fields = ["id", "first_name", "last_name", "email", "is_main"]
        read_only_fields = ["id"]


class ReservationInvoiceDetailsSerializer(serializers.ModelSerializer):
    """Serializer for reservation invoice details objects."""

    reservation = serializers.PrimaryKeyRelatedField(queryset=HotelRoomReservation.objects.all())

    class Meta:
        model = ReservationInvoiceDetails
        fields = ["id", "invoice_date", "invoice_number", "total_amount", "payment_method", "reservation"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a new reservation invoice details."""
        return ReservationInvoiceDetails.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update a reservation invoice details."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class HotelRoomReservationSerializer(serializers.ModelSerializer):
    """Serializer for hotel room reservation objects."""

    room = serializers.PrimaryKeyRelatedField(queryset=HotelRoom.objects.all())
    guests = ReservationGuestDetailsSerializer(many=True)
    invoice = ReservationInvoiceDetailsSerializer(required=False, read_only=True)

    class Meta:
        model = HotelRoomReservation
        fields = ["id", "status", "check_in_date", "check_out_date", "room", "guests", "invoice"]
        read_only_fields = ["id", "invoice"]

    def _create_guests(self, guests, reservation):
        """Handle getting or creating guests as needed."""
        for guest_data in guests:
            ReservationGuestDetails.objects.create(
                reservation=reservation,
                **guest_data,
            )

    def create(self, validated_data):
        """Create a new hotel room reservation."""
        guests = validated_data.pop("guests", [])
        reservation = HotelRoomReservation.objects.create(**validated_data)
        self._create_guests(guests, reservation)
        return reservation

    def update(self, instance, validated_data):
        """Update a hotel room reservation."""
        guests = validated_data.pop("guests", None)
        if guests is not None:
            instance.guests.delete()
            self._create_guests(guests, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
