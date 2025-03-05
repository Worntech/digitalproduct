from django.db import models
from django.conf import settings
import re  # ✅ ADD THIS LINE

from django.contrib.auth import get_user_model
import uuid
    
User = get_user_model()

class ChatRoom(models.Model):
    mystatus = (
            ('Active', 'Active'),
			('Inactive', 'Inactive'),
			)
    name = models.CharField(max_length=255, unique=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=mystatus)
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code

        # 🔹 Format room name BEFORE saving (replace spaces and special characters)
        self.name = re.sub(r'[^a-zA-Z0-9._-]', '_', self.name.strip())

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.unique_code})"  # Include unique_code in the string representation

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
