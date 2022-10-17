from django.views.generic.list import ListView
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_total, summary_total_queryset, summary_per_year, summary_per_month


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            from_date = form.cleaned_data.get("date")
            to_date = form.cleaned_data.get("date_to_field")
            categories = form.cleaned_data.get("category")
            if name:
                queryset = queryset.filter(name__icontains=name)
            if from_date:
                queryset = queryset.filter(date__gte=from_date)
            if to_date:
                queryset = queryset.filter(date__lte=to_date)
            if categories:
                queryset = queryset.filter(category__in=list(map(int, categories)))
            if self.request.GET.get("sorting_by_category") == "ascending":
                queryset = queryset.order_by("category")
            elif self.request.GET.get("sorting_by_category") == "descending":
                queryset = queryset.order_by("-category")
            if self.request.GET.get("sorting_by_date") == "ascending":
                queryset = queryset.order_by("date")
            elif self.request.GET.get("sorting_by_date") == "descending":
                queryset = queryset.order_by("-date")

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_total_queryset=summary_total_queryset(queryset),
            summary_total=summary_total(),
            summary_per_year=summary_per_year(),
            summary_per_month=summary_per_month(),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5
