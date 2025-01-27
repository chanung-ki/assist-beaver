
from django.urls import path
from .views import shipping, table, separate_address

urlpatterns = [
    path('shipping', shipping, name='msk_shipping'),
    path('table', table, name='msk_table'),
    
    path('separate-address', separate_address, name='separate_address'),
]
