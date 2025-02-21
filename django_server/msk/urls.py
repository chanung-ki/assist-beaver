
from django.urls import path
from .views import shipping_task, shipping_total, table, separate_address, convert_shipping_file

urlpatterns = [
    path('shipping/task', shipping_task, name='shipping_task'),
    path('shipping/total', shipping_total, name='shipping_total'),
    path('table', table, name='msk_table'),
    path('separate-address', separate_address, name='separate_address'),
    path('convert/shipping-file', convert_shipping_file, name='convert_shipping_file'),
]
