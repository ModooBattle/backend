from rest_framework import serializers

from users.serializers import UserInfoSerializer

from .models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MessageSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("receiver", "content")


class ChatRoomDetailSerializer(serializers.Serializer):
    chatroom_id = serializers.IntegerField()
    page_no = serializers.IntegerField(help_text="페이지 No")
    length = serializers.IntegerField(help_text="페이지 당 데이터 수")


class MessageReadSerializer(serializers.Serializer):
    chatroom_id = serializers.IntegerField()


class GetChatRoomListSerializer(serializers.Serializer):
    page_no = serializers.IntegerField(help_text="페이지 No")
    length = serializers.IntegerField(help_text="페이지 당 데이터 수")


class ChatRoomListSerializer(serializers.ModelSerializer):
    # unread_cnt = serializers.SerializerMethodField(method_name="get_attributes_count", help_text="안읽은메시지수")
    talker1 = UserInfoSerializer()
    talker2 = UserInfoSerializer()

    class Meta:
        model = ChatRoom
        fields = "__all__"

    # def get_attributes_count(self, instance):
    #     last_message = instance.chatroom.filter(receiver_read=False).count()
    #     return last_message
