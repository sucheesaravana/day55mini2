from django.urls import path
from . import views


urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path(
        'transactions/',
        views.transaction_list,
        name='transaction_list'
    ),

    path(
        'transactions/create/',
        views.transaction_create,
        name='transaction_create'
    ),

    path(
        'transactions/update/<int:pk>/',
        views.transaction_update,
        name='transaction_update'
    ),

    path(
        'transactions/delete/<int:pk>/',
        views.transaction_delete,
        name='transaction_delete'
    ),
]