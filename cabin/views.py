import calendar
from datetime import date, timedelta
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BookingForm
from .models import Booking


@login_required
def dashboard(request):
    selected_year = int(request.GET.get('year', date.today().year))

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect(f"{request.path}?year={booking.start_date.year}")
    else:
        form = BookingForm()

    bookings = Booking.objects.filter(start_date__year__lte=selected_year, end_date__year__gte=selected_year)
    calendar_data = build_year_calendar(selected_year, bookings)

    venmo_link = (
        f"https://venmo.com/{settings.CABIN_VENMO_HANDLE}"
        f"?txn=pay&amount={settings.CABIN_NIGHTLY_RATE}&note={quote('Cabin stay payment')}"
    )

    return render(
        request,
        'cabin/dashboard.html',
        {
            'form': form,
            'calendar_data': calendar_data,
            'selected_year': selected_year,
            'bookings': Booking.objects.order_by('-created_at')[:20],
            'nightly_rate': settings.CABIN_NIGHTLY_RATE,
            'venmo_link': venmo_link,
        },
    )


def build_year_calendar(year, bookings):
    booked_days = set()
    for booking in bookings:
        cursor = booking.start_date
        while cursor <= booking.end_date:
            if cursor.year == year:
                booked_days.add(cursor)
            cursor += timedelta(days=1)

    months = []
    calendar_builder = calendar.Calendar(firstweekday=0)  # Monday

    for month in range(1, 13):
        month_name = calendar.month_name[month]
        weeks = []
        for week in calendar_builder.monthdatescalendar(year, month):
            week_days = []
            for day in week:
                in_month = day.month == month
                is_booked = day in booked_days if in_month else False
                week_days.append(
                    {
                        'day': day.day if in_month else '',
                        'in_month': in_month,
                        'status': 'booked' if is_booked else 'available',
                    }
                )
            weeks.append(week_days)

        months.append({'name': month_name, 'weeks': weeks})

    return months
