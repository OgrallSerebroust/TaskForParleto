from collections import OrderedDict
from .models import Expense
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's')
    ))


def summary_total_queryset(queryset):
    return queryset.aggregate(Sum("amount"))


def summary_total():
    return Expense.objects.all().aggregate(Sum("amount"))
