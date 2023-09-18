from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    expense_date = models.DateField()
    expense_description = models.CharField(max_length=255)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.expense_date} - {self.expense_description} - ${self.expense_amount}"
