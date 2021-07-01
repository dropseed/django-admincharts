# django-admincharts

Chart.js integration for Django admin models

![django-admincharts example](https://user-images.githubusercontent.com/649496/124193149-f3c4c380-da8b-11eb-95d9-74e4f81c4c0a.png)

```python
from django.contrib import admin

from .models import BillingAccount
from admincharts.admin import AdminChartMixin
from admincharts.utils import months_between_dates


@admin.register(BillingAccount)
class BillingAccountAdmin(AdminChartMixin, admin.ModelAdmin):
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
```
