from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('go_to_form',views.go_to_form, name='go_to_form'),
    path('account_form',views.account_form, name='account_form'),
    path('profile/<username>/',views.profile,name='profile'),
    path('update_details/<username>/',views.update_details,name='update_details'),
    path('update_password/<username>/',views.update_password,name='update_password'),
    path('delete_profile/<username>/',views.delete_profile,name='delete_profile'),
    path('expense/<username>/',views.expense,name='expense'),
    path('expense/<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
    path('update_expense/<int:expense_id>',views.update_expense,name= 'update_expense'),
]
