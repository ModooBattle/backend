from django.contrib import admin

from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "talker1", "talker2", "updated_at", "talker1_unread_count", "talker2_unread_count")
    search_fields = ("id",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "chat_room",
        "content",
        "sender",
        "receiver",
        "receiver_read",
        "created_at",
    )
    search_fields = ("id",)
