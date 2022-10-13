from django import forms
from .models import Expense


class ExpenseSearchForm(forms.ModelForm):
    date_to_field = forms.DateField(label="To date:")
    field_order = ["name", "date", "date_to_field", "category"]

    class Meta:
        model = Expense
        fields = ('name', "date", "category")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields["date"].required = False
        self.fields["date"].label = "From date:"
        self.fields["date_to_field"].required = False
        self.fields["category"].required = False
