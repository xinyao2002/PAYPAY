from rest_framework import generics, permissions
from .models import Bill
from .serializers import BillSer
from .services import create_bill

class BillListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BillSer

    def get_queryset(self):
        
        return Bill.objects.filter(splits__user=self.request.user).distinct()

    def perform_create(self, serializer):
        
        create_bill(serializer, self.request)
