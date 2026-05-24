from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils.timezone import now

from .models import Transaction
from .forms import TransactionForm


# Dashboard View
def dashboard(request):

    current_month = now().month
    current_year = now().year

    # Monthly Income
    total_income = Transaction.objects.filter(
        transaction_type='Income',
        date__month=current_month,
        date__year=current_year
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Monthly Expense
    total_expense = Transaction.objects.filter(
        transaction_type='Expense',
        date__month=current_month,
        date__year=current_year
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Net Balance
    net_balance = total_income - total_expense

    # Category Breakdown
    category_breakdown = (
        Transaction.objects
        .filter(transaction_type='Expense')
        .values('category__name')
        .annotate(total_spent=Sum('amount'))
        .order_by('-total_spent')
    )

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'category_breakdown': category_breakdown,
    }

    return render(request, 'mini2/dashboard.html', context)


# List Transactions
def transaction_list(request):

    transactions = Transaction.objects.all().order_by('-date')

    return render(
        request,
        'mini2/transaction_list.html',
        {'transactions': transactions}
    )


# Create Transaction
def transaction_create(request):

    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('transaction_list')

    else:
        form = TransactionForm()

    return render(
        request,
        'mini2/transaction_form.html',
        {'form': form}
    )


# Update Transaction
def transaction_update(request, pk):

    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)

        if form.is_valid():
            form.save()
            return redirect('transaction_list')

    else:
        form = TransactionForm(instance=transaction)

    return render(
        request,
        'mini2/transaction_form.html',
        {'form': form}
    )


# Delete Transaction
def transaction_delete(request, pk):

    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')

    return render(
        request,
        'mini2/transaction_delete.html',
        {'transaction': transaction}
    )