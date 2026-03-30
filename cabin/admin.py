from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'amount_due', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('start_date',)
