from django.shortcuts import render, redirect
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import Transaction
from .forms import TransactionForm


def add_transaction(request):

    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = TransactionForm()

    return render(
        request,
        'mini2/add_transaction.html',
        {'form': form}
    )


def dashboard(request):

    current_month = timezone.now().month
    current_year = timezone.now().year

    income = Transaction.objects.filter(
        transaction_type='Income',
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))

    expense = Transaction.objects.filter(
        transaction_type='Expense',
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))

    total_income = income['total'] or 0
    total_expense = expense['total'] or 0

    net_balance = total_income - total_expense

    transactions = Transaction.objects.all()

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'transactions': transactions,
    }

    return render(
        request,
        'mini2/dashboard.html',
        context
    )


def category_breakdown(request):

    categories = (
        Transaction.objects
        .filter(transaction_type='Expense')
        .values('category__name')
        .annotate(total_spent=Sum('amount'))
    )

    return render(
        request,
        'mini2/category_breakdown.html',
        {'categories': categories}
    )