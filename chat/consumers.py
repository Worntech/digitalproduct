import json
import re
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles new WebSocket connections"""
        # Retrieve the unique_code from the URL
        self.unique_code = self.scope["url_route"]["kwargs"]["unique_code"].strip()

        # Get or create the chat room using unique_code
        self.room = await sync_to_async(ChatRoom.objects.get)(unique_code=self.unique_code)
        self.room_group_name = f"chat_{self.room.unique_code}"

        # Get the authenticated user
        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        # Add the user to the chat group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Handles WebSocket disconnections"""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles receiving messages from WebSocket"""
        data = json.loads(text_data)
        content = data.get("content", "").strip()
        sender_username = data.get("sender", "")

        if not sender_username or not content:
            return  # Ignore empty messages

        # Get sender user object
        sender = await sync_to_async(User.objects.get)(username=sender_username)

        # Save message to database
        message = await sync_to_async(Message.objects.create)(
            room=self.room,
            sender=sender,
            content=content
        )

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "content": message.content,
                "sender": sender.username,
                "timestamp": message.timestamp.isoformat(),
            }
        )

    async def chat_message(self, event):
        """Sends messages to WebSocket"""
        await self.send(text_data=json.dumps({
            "content": event["content"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))
