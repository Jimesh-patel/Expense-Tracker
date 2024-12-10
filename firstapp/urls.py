from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.base_view, name='base_view'),
    path('signupForm_view/', views.signupForm_view, name='signupForm_view'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('add_group/', views.add_group, name='add_group'),
    path('group_view/', views.group_view, name='group_view'),
    path('add_group_members/', views.add_group_members, name='add_group_members'),
    path('add_group_expense_record/', views.add_group_expense_record, name='add_group_expense_record'),
    path('show_settlement_view/settlement_view', views.settlement_view, name='settlement_view'),
    path('dashboard1_view/', views.dashboard1_view, name='dashboard1_view'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_expense_form/', views.add_expense_form, name='add_expense_form'),
    path('group_settlement_view/', views.group_settlement_view, name='group_settlement_view'),
    path('add_expense_separate/', views.add_expense_separate, name='add_expense_separate'),
    path('clear_records/', views.clear_records, name='clear_records'),
    
]
