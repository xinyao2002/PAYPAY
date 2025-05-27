from django.db import transaction
from .models import Bill, BillSplit

@transaction.atomic
def create_bill(serializer, request):
    splits_data = request.data.get("splits", [])
    bill = serializer.save(created_by=request.user)
    for s in splits_data:
        BillSplit.objects.create(
            bill=bill,
            user_id=s["user_id"],
            amount=s["amount"],
        )
    return bill

def accept_split(user, bill_id):
    split = BillSplit.objects.select_for_update().get(bill_id=bill_id, user=user)
    split.agree = True
    split.responded_at = timezone.now()
    split.save(update_fields=["agree", "responded_at"])

def reject_split(user, bill_id):
    split = BillSplit.objects.select_for_update().get(bill_id=bill_id, user=user)
    split.agree = False
    split.responded_at = timezone.now()
    split.save(update_fields=["agree", "responded_at"])

def update_amount(user, bill_id, amount):
    split = BillSplit.objects.select_for_update().get(bill_id=bill_id, user=user)
    split.amount = amount
    split.save(update_fields=["amount"])

def bill_snapshot(bill_id):
    bill = Bill.objects.prefetch_related("splits__user").get(id=bill_id)
    from .serializers import BillSer
    return BillSer(bill).data
