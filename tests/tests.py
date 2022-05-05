from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.utils import timezone

from accounts.admin import AccountAdmin
from accounts.models import Account


class MockChangelist:
    def __init__(self, queryset):
        self.queryset = queryset
        self.result_list = queryset  # Would be the paginated list of objects


class AdminTest(TestCase):
    def setUp(self):
        Account.objects.create(
            name="1",
            ctime=timezone.datetime(
                year=2021,
                month=7,
                day=1,
                hour=1,
                minute=1,
                second=1,
                microsecond=1,
            ),
        )
        self.model_admin = AccountAdmin(model=Account, admin_site=AdminSite())

    def test_admin(self):
        queryset = self.model_admin.get_list_chart_queryset(
            MockChangelist(Account.objects.all())
        )
        self.assertEquals(self.model_admin.get_list_chart_type(queryset), "bar")
        chart_data = self.model_admin.get_list_chart_data(queryset)
        self.assertIn("labels", chart_data)
        self.assertEquals(len(chart_data["datasets"]), 1)

        self.assertEquals(
            self.model_admin.get_list_chart_options(queryset), {"aspectRatio": 6}
        )


class AdminEmptyTest(TestCase):
    def setUp(self):
        self.model_admin = AccountAdmin(model=Account, admin_site=AdminSite())

    def test_admin(self):
        queryset = self.model_admin.get_list_chart_queryset(
            MockChangelist(Account.objects.all())
        )
        self.assertEquals(self.model_admin.get_list_chart_type(queryset), "bar")
        self.assertEquals(self.model_admin.get_list_chart_data(queryset), {})
        self.assertEquals(
            self.model_admin.get_list_chart_options(queryset), {"aspectRatio": 6}
        )
