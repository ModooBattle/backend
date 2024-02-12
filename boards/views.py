from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, exceptions, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

from .models import Comment, Post, Reply
from .serializers import (
    CommentIDSerializer,
    CommentPutSerializer,
    CommentSerializer,
    CommentWriteSerializer,
    PostIDSerializer,
    PostInfoSerializer,
    PostPatchSerializer,
    PostPutSerializer,
    PostQuerySerializer,
    PostSerializer,
    PostWriteSerializer,
    ReplyIDSerializer,
    ReplyPutSerializer,
    ReplySerializer,
    ReplyWriteSerializer,
)

swagger_tag = "게시판"


@decorators.permission_classes([permissions.IsAuthenticated])
class BoardView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="게시물 목록 조회 및 검색",
        query_serializer=PostQuerySerializer,
        responses={200: "ok"},
    )
    def get(self, request):
        """
        댓글과 대댓글도 한번에 조회됩니다
        """
        sport = request.GET["sport_id"]
        page_no = request.GET["page_no"]
        length = request.GET["length"]
        search_category = request.GET.get("search_category", None)
        search_value = request.GET.get("search_value", None)
        order_by = request.GET.get("order_by", "updated_at")
        try:
            if search_category and search_value:
                if search_category == "title":
                    posts = Post.objects.filter(category=sport, title__contains=search_value).order_by(f"-{order_by}")

                elif search_category == "content":
                    posts = Post.objects.filter(category=sport, content__contains=search_value).order_by(
                        f"-{order_by}"
                    )
                elif search_category == "writer":
                    posts = Post.objects.filter(category=sport, writer__username__contains=search_value).order_by(
                        f"-{order_by}"
                    )
                else:
                    return Response(
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        data="search_category : title or content or writer",
                    )

            else:
                posts = Post.objects.filter(category=sport).order_by(f"-{order_by}")
            paginator = Paginator(posts, int(length))
            page_obj = paginator.get_page(int(page_no))
            serializer = PostInfoSerializer(page_obj, many=True)

            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="this post list does not exist")

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="게시글 등록",
        request_body=PostWriteSerializer,
        responses={"200": "ok", "401": "unauthorized"},
    )
    def post(self, request):
        data = request.data.copy()
        user_id = request.user.id

        try:
            sport_id = User.objects.get(id=user_id).sport.id
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="this user does not exist")

        data["writer"] = user_id
        data["category"] = sport_id

        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="게시글 수정",
        request_body=PostPutSerializer,
        responses={"200": "ok", "401": "unauthorized", "403": "current_user is not author"},
    )
    def put(self, request):
        data = request.data.copy()

        post = Post.objects.get(id=data["post_id"])
        writer = post.writer.id
        user_id = request.user.id

        if writer != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="게시글 조회수 또는 좋아요 수 +1",
        request_body=PostPatchSerializer,
        responses={"200": "ok", "401": "unauthorized"},
    )
    def patch(self, request):
        data = request.data.copy()

        post = Post.objects.get(id=data["post_id"])
        target = Post.objects.get(id=data["target"])

        if target == "like":
            post.like_count += 1

        else:
            post.view_count += 1
        post.save()

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="게시글 삭제",
        request_body=PostIDSerializer,
        responses={"200": "ok", "401": "unauthorized", "403": "current_user is not author"},
    )
    def delete(self, request):
        data = request.data.copy()

        post = Post.objects.get(id=data["post_id"])
        writer = post.writer.id
        user_id = request.user.id

        if writer != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        post.delete()

        return Response(status=status.HTTP_200_OK)


@decorators.permission_classes([permissions.IsAuthenticated])
class CommentView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="댓글 등록",
        request_body=CommentWriteSerializer,
        responses={"200": "ok", "401": "unauthorized"},
    )
    def post(self, request):
        data = request.data.copy()
        user_id = request.user.id

        data["writer"] = user_id

        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="댓글 수정",
        request_body=CommentPutSerializer,
        responses={"200": "ok", "401": "unauthorized", "403": "current_user is not author"},
    )
    def put(self, request):
        data = request.data.copy()

        comment = Comment.objects.get(id=data["comment_id"])
        writer = comment.writer.id
        user_id = request.user.id

        if writer != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(comment, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="댓글 삭제",
        request_body=CommentIDSerializer,
        responses={"200": "ok", "401": "unauthorized", "403": "current_user is not author"},
    )
    def delete(self, request):
        data = request.data.copy()

        comment = Comment.objects.get(id=data["comment_id"])
        writer = comment.writer.id
        user_id = request.user.id

        if writer != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        comment.delete()

        return Response(status=status.HTTP_200_OK)


@decorators.permission_classes([permissions.IsAuthenticated])
class ReplyView(APIView):
    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="대댓글 등록",
        request_body=ReplyWriteSerializer,
        responses={"200": "ok", "401": "unauthorized"},
    )
    def post(self, request):
        data = request.data.copy()
        user_id = request.user.id

        data["writer"] = user_id

        serializer = ReplySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="대댓글 수정",
        request_body=CommentPutSerializer,
        responses={"200": "ok", "401": "unauthorized", "403": "current_user is not author"},
    )
    def put(self, request):
        data = request.data.copy()

        reply = Reply.objects.get(id=data["reply_id"])
        writer = reply.writer.id
        user_id = request.user.id

        if writer != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(reply, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=[swagger_tag],
        operation_summary="대댓글 삭제",
        request_body=ReplyIDSerializer,
        responses={"200": "ok", "401": "unauthorized", "403": "current_user is not author"},
    )
    def delete(self, request):
        data = request.data.copy()

        reply = Reply.objects.get(id=data["reply_id"])
        writer = reply.writer.id
        user_id = request.user.id

        if writer != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        reply.delete()

        return Response(status=status.HTTP_200_OK)
