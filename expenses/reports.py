from collections import OrderedDict
from .models import Expense
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce, TruncMonth, TruncYear


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
    return Expense.objects.aggregate(Sum("amount"))


def summary_per_year():
    return Expense.objects.annotate(year=TruncYear("date")).values("year").annotate(
        amount_sum=Sum("amount")).values_list("year", "amount_sum").order_by("-year")


def summary_per_month():
    return Expense.objects.annotate(month=TruncMonth("date")).values("month").annotate(
        amount_sum=Sum("amount")).values_list("month", "amount_sum").order_by("-month")
