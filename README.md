# django-admincharts

Add [Chart.js](https://www.chartjs.org/docs/latest/) visualizations to your Django admin using a mixin class.

## Example

![django-admincharts example](https://user-images.githubusercontent.com/649496/124196798-c3ccee80-da92-11eb-9c2a-c0f94171d071.png)

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

## Installation

Install from [pypi.org](https://pypi.org/project/django-admincharts/):

```console
$ pip install django-admincharts
```

Add `admincharts` to your Django `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "admincharts",
]
```

Use the `AdminChartMixin` with an `admin.ModelAdmin` class to add a chart to the changelist view.

Options can be set directly on the class:

```python
from django.contrib import admin
from admincharts.admin import AdminChartMixin

@admin.register(MyModel)
class MyModelAdmin(AdminChartMixin, admin.ModelAdmin):
    list_chart_type = "bar"
    list_chart_data = {}
    list_chart_options = {"aspectRatio": 6}
    list_chart_config = None  # Override the combined settings
```

Or by using the class methods which gives you access to the queryset being used for the current view:

```python
class MyModelAdmin(AdminChartMixin, admin.ModelAdmin):
    def get_list_chart_queryset(self, changelist):
        ...

    def get_list_chart_type(self, queryset):
        ...

    def get_list_chart_data(self, queryset):
        ...

    def get_list_chart_options(self, queryset):
        ...

    def get_list_chart_config(self, queryset):
        ...
```

The `type`, `data`, and `options` are passed directly to Chart.js to render the chart.
[Look at the Chart.js docs to see what kinds of settings can be used.](https://www.chartjs.org/docs/latest/configuration/)

By default, the objects in your chart will be the objects that are currently visible in your list view.
This means that admin controls like [search](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields) and [list filter](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter) will update your chart,
and you can use the Django [pagination](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_per_page) [settings](https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_max_show_all) to control how many objects you want in your chart at a time.
To ignore pagination but still respect search/filter,
you can override the `get_list_chart_queryset` method to return the full queryset:

```python
class MyModelAdmin(AdminChartMixin, admin.ModelAdmin):
    def get_list_chart_queryset(self, changelist):
        return changelist.queryset
```

And if you want, you can also sidestep the list queryset entirely by using overriding `get_list_chart_queryset` with your own query:

```python
class MyModelAdmin(AdminChartMixin, admin.ModelAdmin):
    def get_list_chart_queryset(self, changelist):
        return MyModel.objects.all()
```
