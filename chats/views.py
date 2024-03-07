from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, exceptions, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

from .models import ChatRoom, Message
from .serializers import (
    ChatRoomDetailSerializer,
    ChatRoomListSerializer,
    GetChatRoomListSerializer,
    MessageReadSerializer,
    MessageSendSerializer,
    MessageSerializer,
)

swagger_tag = "채팅"


@decorators.permission_classes([permissions.IsAuthenticated])
class ChatRoomListView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="전체 채팅방 조회",
        query_serializer=GetChatRoomListSerializer,
        responses={200: "ok"},
    )
    def get(self, request):
        user_id = request.user.id
        page_no = request.GET["page_no"]
        length = request.GET["length"]

        try:
            chatrooms = ChatRoom.objects.filter(Q(talker1=user_id) | Q(talker2=user_id)).order_by("-updated_at")

            paginator = Paginator(chatrooms, int(length))
            page_obj = paginator.get_page(int(page_no))

            serializer = ChatRoomListSerializer(page_obj, many=True)

            for d in serializer.data:
                if d["talker1"]["id"] == user_id:
                    d["talker"] = d["talker2"]
                    d["unread_count"] = d["talker1_unread_count"]
                else:
                    d["talker"] = d["talker1"]
                    d["unread_count"] = d["talker2_unread_count"]

                del d["talker1"]
                del d["talker2"]
                del d["talker1_unread_count"]
                del d["talker2_unread_count"]

            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ChatRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="this ChatRoom list does not exist")


@decorators.permission_classes([permissions.IsAuthenticated])
class ChatRoomDetailView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="채팅내용 조회",
        query_serializer=ChatRoomDetailSerializer,
        responses={200: "ok"},
    )
    def get(self, request):
        user_id = request.user.id
        chatroom_id = request.GET["chatroom_id"]
        page_no = request.GET["page_no"]
        length = request.GET["length"]

        try:
            messages = Message.objects.filter(chat_room=chatroom_id).order_by("-created_at")

            paginator = Paginator(messages, int(length))
            page_obj = paginator.get_page(int(page_no))

            serializer = MessageSerializer(page_obj, many=True)

            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ChatRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="this ChatRoom list does not exist")

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="채팅보내기",
        request_body=MessageSendSerializer,
        responses={"200": "ok", "401": "unauthorized"},
    )
    def post(self, request):
        data = request.data.copy()
        user_id = request.user.id
        with transaction.atomic():
            try:
                receiver = User.objects.get(id=data["receiver"])
                sender = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data="this receiver does not exist")

            try:
                chatroom_id = ChatRoom.objects.get(talker1=user_id, talker2=data["receiver"]).id

            except ChatRoom.DoesNotExist:
                try:
                    chatroom_id = ChatRoom.objects.get(talker2=user_id, talker1=data["receiver"]).id

                except ChatRoom.DoesNotExist:
                    chatroom = ChatRoom.objects.create(talker1=sender, talker2=receiver)
                    chatroom_id = chatroom.id
            data["chat_room"] = chatroom_id
            data["sender"] = user_id

            serializer = MessageSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            chatroom = ChatRoom.objects.get(id=chatroom_id)
            chatroom.updated_at = timezone.now()

            if chatroom.talker1_id == user_id:
                chatroom.talker2_unread_count += 1

            else:
                chatroom.talker1_unread_count += 1
            chatroom.save()

            return Response(status=status.HTTP_200_OK, data={"chatroom_id": chatroom_id})

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="채팅읽기",
        query_serializer=MessageReadSerializer,
        responses={"200": "ok", "401": "unauthorized"},
    )
    def patch(self, request):
        user_id = request.user.id
        chatroom_id = request.GET["chatroom_id"]

        with transaction.atomic():
            chatroom = ChatRoom.objects.get(id=chatroom_id)
            chatroom.chatroom.filter(receiver_id=user_id).update(receiver_read=True)

            if chatroom.talker1_id == user_id:
                chatroom.talker1_unread_count = 0
            else:
                chatroom.talker2_unread_count = 0
            chatroom.save()

            return Response(status=status.HTTP_200_OK)
