from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction

        fields = [
            'transaction_type',
            'category',
            'date',
            'amount',
            'description'
        ]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }