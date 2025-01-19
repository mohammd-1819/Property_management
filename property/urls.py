from django.urls import path
from .views import property, transaction, city, booking

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
    path('transaction/detail/<int:transaction_id>/', transaction.TransactionDetailView.as_view(),
         name='transaction-detail'),

    path('city/list/', city.CityListView.as_view(), name='city-list'),
    path('city/detail/<str:city_name>', city.CityDetailView.as_view(), name='city-detail'),
    path('city/create/', city.CreateCityView.as_view(), name='city-create'),
    path('city/update/<str:city_name>/', city.UpdateCityView.as_view(), name='city-update'),
    path('city/remove/<str:city_name>/', city.RemoveCityView.as_view(), name='city-remove'),

    path('booking/list/', booking.BookingListView.as_view(), name='booking-list'),
    path('booking/detail/<int:booking_id>/', booking.BookingDetailView.as_view(), name='booking-detail'),
    path('booking/update/<int:booking_id>/', booking.UpdateBookingRequestView.as_view(), name='booking-update'),
    path('booking/remove/<int:booking_id>/', booking.RemoveBookingRequestView.as_view(), name='booking-delete'),
    path('booking/request/', booking.CreateBookingRequestView.as_view(), name='booking-create'),

]
