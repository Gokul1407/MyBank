from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .forms import UpdateDetailsForm,UpdatePasswordForm,ExpenseForm,UpdateExpense
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required




# Create your views here.

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        if password == repeat_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken")
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                messages.success(request, "Registration successful. You can now log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "registration.html")


def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('go_to_form')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def go_to_form(request):
    return render(request, 'go_to_form.html')


def account_form(request):
    return render(request, 'account_form.html')


def profile(request,username):
    username = User.username
    return render(request,'profile.html')


def update_details(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        # Handle form submission to update user details here
        # You can use Django Forms for this purpose

        form = UpdateDetailsForm(request.POST or None)
        if form.is_valid():

            new_username = form.cleaned_data['username']
            new_email = form.cleaned_data['email']

            user.username = new_username
            user.email = new_email
            user.save()

            messages.success(request, "Profile updated successfully")
            return redirect('profile', username=username)
        else:
            messages.error(request, "Error updating profile")
            return redirect('profile', username=username)

    else:
        # Create a form instance for GET requests
        form = UpdateDetailsForm()

    return render(request, 'update_details.html', {'user': user, 'form': form})
    


def update_password(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        # Handle form submission to update user details here
        # You can use Django Forms for this purpose

        form = UpdatePasswordForm(request.POST or None)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            new_repeat_password = form.cleaned_data['repeat_password']

            if new_password == new_repeat_password:
                user.set_password(new_password)  # Update the user's password
                user.save()
                update_session_auth_hash(request, user)  # Update the session with the new password
                messages.success(request, "Password changed successfully. You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match")
                return redirect('profile', username=username)


        else:
            messages.error(request, "Error updating Password")
            return redirect('profile', username=username)

    else:
        # Create a form instance for GET requests
        form = UpdatePasswordForm()

    return render(request, 'update_password.html', {'user': user, 'form': form})



def delete_profile(request,username):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        user.delete()
        return redirect('/')
    return render(request,'delete_profile.html')

    

from django.contrib.auth.decorators import login_required

@login_required
def expense(request, username):
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by('-expense_date')

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # Save the expense data to the database
            expense = form.save(commit=False)
            expense.user = user  # Set the user for the expense
            expense.save()
            form = ExpenseForm()  # Reset the form after saving
            messages.success(request, "Expense added successfully")
        else:
            # Debugging: Print form errors to the console
            print(form.errors)
            messages.error(request, "Error adding expense. Please check the data.")

    else:
        form = ExpenseForm()

    return render(request, 'expense.html', {'form': form, 'expenses': expenses})



@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted successfully")
    else:
        messages.error(request, "Invalid request")

    return redirect('expense', username=request.user.username)


@login_required
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        form = UpdateExpense(request.POST, instance=expense) 
        if form.is_valid():
            form.save() 
            messages.success(request, "Expense updated successfully")
            return redirect('expense', username=request.user.username)  
        else:
            messages.error(request, "Error updating expense. Please check the data.")
    else:
        form = UpdateExpense(instance=expense)  

    return render(request, 'update_expense.html', {'form': form, 'expense': expense})
