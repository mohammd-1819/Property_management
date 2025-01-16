from django.urls import path
from .views import property, transaction

app_name = 'property'

urlpatterns = [
    path('list/', property.PropertyListView.as_view(), name='property-list'),
    path('detail/<str:property_title>/', property.PropertyDetailView.as_view(), name='property-detail'),
    path('create/', property.CreatePropertyView.as_view(), name='property-create'),
    path('update/<str:property_title>/', property.PropertyUpdateView.as_view(), name='property-update'),
    path('delete/<str:property_title>/', property.DeletePropertyView.as_view(), name='property-delete'),

    path('transaction/list/', transaction.TransactionListView.as_view(), name='transaction-list'),
    path('transaction/user/', transaction.UserTransactionView.as_view(), name='transaction-user'),
    path('transaction/create/', transaction.CreateTransaction.as_view(), name='transaction-create'),
    path('transaction/detail/<int:transaction_id>', transaction.TransactionDetailView.as_view(),
         name='transaction-detail'),

]
