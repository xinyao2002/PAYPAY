from django.urls import path
from .views import BillListCreate
urlpatterns = [
    path("bills/", BillListCreate.as_view(), name="bill-list-create"),
]
