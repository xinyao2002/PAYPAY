from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import BillSplit
from .services import accept_split, reject_split, update_amount, bill_snapshot

class BillConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.bill_id = self.scope["url_route"]["kwargs"]["bill_id"]
        self.group_name = f"bill_{self.bill_id}"
        user = self.scope["user"]

        # 鉴权：必须是账单参与者
        is_member = await database_sync_to_async(
            BillSplit.objects.filter(bill_id=self.bill_id, user=user).exists
        )()
        if not (user.is_authenticated and is_member):
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # 连接后立即把当前状态发给客户端
        state = await database_sync_to_async(bill_snapshot)(self.bill_id)
        await self.send_json(state)

    async def receive_json(self, content):
        user = self.scope["user"]
        t = content.get("type")
        if t == "accept":
            await database_sync_to_async(accept_split)(user, self.bill_id)
        elif t == "reject":
            await database_sync_to_async(reject_split)(user, self.bill_id)
        elif t == "update_amount":
            await database_sync_to_async(update_amount)(
                user, self.bill_id, content["amount"]
            )
        # 其余动作都在信号里统一广播，Consumer 里不直接发

    async def broadcast_state(self, event):
        await self.send_json(event["data"])

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
