from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if not start_date or not end_date:
            return cleaned_data

        if end_date < start_date:
            raise ValidationError('End date must be the same day or after start date.')

        overlap = Booking.objects.filter(start_date__lte=end_date, end_date__gte=start_date)
        if self.instance.pk:
            overlap = overlap.exclude(pk=self.instance.pk)
        if overlap.exists():
            raise ValidationError('Those dates overlap with an existing booking.')

        nights = (end_date - start_date).days + 1
        cleaned_data['amount_due'] = nights * settings.CABIN_NIGHTLY_RATE
        return cleaned_data

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.amount_due = self.cleaned_data['amount_due']
        if commit:
            booking.save()
        return booking
