from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import BookingForm
from .models import Booking


class BookingFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='family', password='pass1234')

    def test_same_day_booking_is_valid(self):
        form = BookingForm(data={'start_date': '2026-07-01', 'end_date': '2026-07-01'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['amount_due'], 25)

    def test_overlap_booking_is_invalid(self):
        Booking.objects.create(
            user=self.user,
            start_date=date(2026, 7, 1),
            end_date=date(2026, 7, 3),
            amount_due=75,
        )
        form = BookingForm(data={'start_date': '2026-07-03', 'end_date': '2026-07-05'})
        self.assertFalse(form.is_valid())
