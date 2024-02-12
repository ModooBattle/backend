from django.db import models


class ChatRoom(models.Model):
    talker1 = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="msg_talker1", blank=True, null=False, help_text="참가자1"
    )
    talker2 = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="msg_talker2", blank=False, null=False, help_text="참가자2"
    )
    updated_at = models.DateTimeField(blank=True, null=True, help_text="작성일")
    talker1_unread_count = models.IntegerField(default=0, blank=True, null=False)
    talker2_unread_count = models.IntegerField(default=0, blank=True, null=False)

    def __str__(self):
        return f"{self.talker1}_{self.talker2}"


class Message(models.Model):
    chat_room = models.ForeignKey(
        "chats.ChatRoom", on_delete=models.CASCADE, related_name="chatroom", blank=True, null=False, help_text="보낸사람"
    )
    content = models.TextField(max_length=500, blank=False, null=False, help_text="게시글 본문")
    sender = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="msg_sender", blank=True, null=False, help_text="보낸사람"
    )
    receiver = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="msg_receiver", blank=False, null=False, help_text="받는사람"
    )

    receiver_read = models.BooleanField(default=False, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, help_text="작성일")

    def __str__(self):
        return self.content
