from django.contrib import admin
from django.utils import timezone

from admincharts.admin import AdminChartMixin
from admincharts.utils import months_between_dates

from .models import Account


@admin.register(Account)
class AccountAdmin(AdminChartMixin, admin.ModelAdmin):
    list_display = ("name", "ctime")
    ordering = ("-ctime",)

    def get_list_chart_data(self, queryset):
        if not queryset:
            return {}

        # Cannot reorder the queryset at this point
        earliest = min([x.ctime for x in queryset])

        labels = []
        totals = []
        for b in months_between_dates(earliest, timezone.now()):
            labels.append(b.strftime("%b %Y"))
            totals.append(
                len(
                    [
                        x
                        for x in queryset
                        if x.ctime.year == b.year and x.ctime.month == b.month
                    ]
                )
            )

        return {
            "labels": labels,
            "datasets": [
                {"label": "New accounts", "data": totals, "backgroundColor": "#79aec8"},
            ],
        }
