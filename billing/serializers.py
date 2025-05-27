from rest_framework import serializers
from .models import Bill, BillSplit

class BillSplitSer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = BillSplit
        fields = ("user", "amount", "agree", "paid")  

class BillSer(serializers.ModelSerializer):
    splits = BillSplitSer(many=True, read_only=True)
    class Meta:
        model = Bill
        fields = ("id", "name", "total_amount", "status", "splits", "created_time")
