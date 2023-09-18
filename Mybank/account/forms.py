from django import forms
from .models import Expense


class UpdateDetailsForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)



class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_date', 'expense_description', 'expense_amount']

class UpdateExpense(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_date', 'expense_description', 'expense_amount']
