# bank/views.py

from django.shortcuts import render, redirect
from .forms import DepositForm, WithdrawForm, CustomUserCreationForm, UserUpdateForm
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from decimal import Decimal

# Dashboard view
def dashboard(request):
    return render(request, 'bank/dashboard.html')

# Deposit view - login required
@login_required(login_url='/login/')
def deposit_view(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            # Get last transaction to calculate current balance
            last_transaction = Transaction.objects.filter(user=request.user).order_by('-date').first()
            current_balance = last_transaction.balance_after_transaction if last_transaction else Decimal('0.00')

            new_balance = current_balance + amount

            # Save transaction with updated balance
            Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_type='deposit',
                balance_after_transaction=new_balance
            )

            return redirect('transactions')
    else:
        form = DepositForm()

    return render(request, 'bank/deposit.html', {'form': form})

# Withdraw view - login required
@login_required(login_url='/login/')
def withdraw_view(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            # Get last transaction to get current balance
            last_transaction = Transaction.objects.filter(user=request.user).order_by('-date').first()
            current_balance = last_transaction.balance_after_transaction if last_transaction else Decimal('0.00')

            # Check if balance is enough
            if amount > current_balance:
                messages.error(request, "Insufficient balance!")
                return render(request, 'bank/withdraw.html', {'form': form})

            new_balance = current_balance - amount

            # Save transaction
            Transaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_type='withdraw',
                balance_after_transaction=new_balance
            )

            return redirect('transactions')
    else:
        form = WithdrawForm()
    
    return render(request, 'bank/withdraw.html', {'form': form})

# Transaction history - login required
@login_required(login_url='/login/')
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

# Signup view (no login required here)
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Logout page (just for displaying, logic can be added later)
def logout_user(request):
    return render(request, 'registration/logout.html')
    # NOTE: The redirect below will never run because of the return above
    # return redirect('dashboard')  

# Profile view - login required
@login_required(login_url='/login/')
def profile_view(request):
    user = request.user
    last_tx = Transaction.objects.filter(user=user).order_by('-date').first()
    balance = last_tx.balance_after_transaction if last_tx else 0
    return render(request, 'bank/profile.html', {'user': user, 'balance': balance})

# Update profile - login required
@login_required(login_url='/login/')
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'bank/update_profile.html', {'form': form})
