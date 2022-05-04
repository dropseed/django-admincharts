from django.contrib.admin import ModelAdmin


class AdminChartMixin:
    change_list_template = "admin/admincharts/generic_change_list.html"

    list_chart_type = "bar"
    list_chart_data = {}
    list_chart_options = {"aspectRatio": 6}
    list_chart_config = None  # Override the combined settings

    class Media:
        css = {"all": ("admincharts/admincharts.css",)}
        js = (
            "admincharts/chart.min.js",
            "admincharts/admincharts.js",
        )

    def get_list_chart_queryset(self, changelist):
        """
        Returns the current changelist.result_list by default which
        is the filtered *and* paginated queryset.
        To ignore pagination, you can return the changelist.queryset instead.
        """
        return changelist.result_list

    def get_list_chart_type(self, queryset):
        return self.list_chart_type

    def get_list_chart_data(self, queryset):
        return self.list_chart_data

    def get_list_chart_options(self, queryset):
        return self.list_chart_options

    def get_list_chart_config(self, queryset):
        if self.list_chart_config:
            return self.list_chart_config

        return {
            "type": self.get_list_chart_type(queryset),
            "data": self.get_list_chart_data(queryset),
            "options": self.get_list_chart_options(queryset),
        }

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        # This could be a redirect and not have context_data
        if not hasattr(response, "context_data"):
            return response

        if "cl" in response.context_data:
            changelist = response.context_data["cl"]
            chart_queryset = self.get_list_chart_queryset(changelist)
            response.context_data["adminchart_queryset"] = chart_queryset
            response.context_data[
                "adminchart_chartjs_config"
            ] = self.get_list_chart_config(chart_queryset)
        else:
            response.context_data["adminchart_queryset"] = None
            response.context_data["adminchart_chartjs_config"] = None

        return response
