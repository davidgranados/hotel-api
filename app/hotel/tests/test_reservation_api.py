"""
Tests for hotel APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import HotelRoom, HotelRoomReservation
from hotel.serializers import HotelRoomReservationSerializer

User = get_user_model()

RESERVATION_URL = reverse("hotel:hotelroomreservation-list")


def detail_url(id):
    """Return reservation detail URL."""
    return reverse("hotel:hotelroomreservation-detail", args=[id])


def create_user(email="example@user.com", password="password"):
    """Create a user."""
    return User.objects.create_user(email, password)


def create_hotel_room(room_number="101"):
    """Create and return a sample hotel room."""
    return HotelRoom.objects.create(room_number=room_number)


class PublicHotelReservationApiTests(TestCase):
    """Test the publicly available hotel reservation APIs."""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving hotel reservation."""
        res_get = self.client.get(RESERVATION_URL)
        res_post = self.client.post(RESERVATION_URL)
        res_put = self.client.put(RESERVATION_URL)
        res_patch = self.client.patch(RESERVATION_URL)
        res_delete = self.client.delete(RESERVATION_URL)

        self.assertEqual(res_get.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res_post.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res_put.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res_patch.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res_delete.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateHotelReservationApiTests(TestCase):
    """Test the authorized user hotel reservation APIs."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_hotel_reservation(self):
        """Test retrieving a list of hotel reservation."""
        room = create_hotel_room()
        room2 = create_hotel_room(room_number="102")
        HotelRoomReservation.objects.create(
            room=room,
            check_in_date="2020-01-01",
            check_out_date="2020-01-02",
        )
        HotelRoomReservation.objects.create(
            room=room2,
            check_in_date="2020-01-03",
            check_out_date="2020-01-04",
        )

        res = self.client.get(RESERVATION_URL)

        reservations = HotelRoomReservation.objects.all()
        serializer = HotelRoomReservationSerializer(reservations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_reservation(self):
        """Test creating a reservation."""
        room = create_hotel_room()
        payload = {
            "room": room.id,
            "check_in_date": "2020-01-01",
            "check_out_date": "2020-01-02",
            "guests": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@doe.com",
                    "is_main": True,
                },
                {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": "jane@doe.com",
                },
            ],
        }
        res = self.client.post(RESERVATION_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        reservation = HotelRoomReservation.objects.get(id=res.data["id"])
        self.assertEqual(reservation.room.id, payload["room"])
        self.assertEqual(reservation.check_in_date.strftime("%Y-%m-%d"), payload["check_in_date"])
        self.assertEqual(reservation.check_out_date.strftime("%Y-%m-%d"), payload["check_out_date"])
        self.assertEqual(reservation.guests.count(), 2)
