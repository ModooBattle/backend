from rest_framework import serializers

from users.serializers import UserInfoSerializer

from .models import Comment, Post, Reply


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content")


class PostPutSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(help_text="게시물 id")

    class Meta:
        model = Post
        fields = ("post_id", "title", "content")


class PostPatchSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(help_text="게시물 id")
    target = serializers.CharField(help_text="변동 항목: like or view")


class PostIDSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(help_text="게시물 id")


class PostQuerySerializer(serializers.Serializer):
    sport_id = serializers.IntegerField(help_text="경기종목 id")
    page_no = serializers.IntegerField(help_text="페이지 No")
    length = serializers.IntegerField(help_text="페이지 당 데이터 수")
    order_by = serializers.CharField(
        required=False, max_length=20, help_text="정렬방식(내림차순): updated_at(업데이트 일시), view_count(조회수), like_count(좋아요 수)"
    )
    search_category = serializers.CharField(
        required=False, max_length=20, help_text="검색 카테고리: title(제목), content(내용), writer(작성자 닉네임)"
    )
    search_value = serializers.CharField(required=False, max_length=20, help_text="검색 내용")


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "content")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentPutSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(help_text="댓글 id")

    class Meta:
        model = Comment
        fields = ("comment_id", "content")


class CommentIDSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField(help_text="댓글 id")


class ReplyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ("comment", "content")


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"


class ReplyPutSerializer(serializers.ModelSerializer):
    reply_id = serializers.IntegerField(help_text="대댓글 id")

    class Meta:
        model = Reply
        fields = ("reply_id", "content")


class ReplyIDSerializer(serializers.Serializer):
    reply_id = serializers.IntegerField(help_text="대댓글 id")


class ReplyInfoSerializer(serializers.ModelSerializer):
    writer = UserInfoSerializer()

    class Meta:
        model = Reply
        fields = "__all__"


class CommentInfoSerializer(serializers.ModelSerializer):
    writer = UserInfoSerializer()
    replies = ReplyInfoSerializer(many=True)

    class Meta:
        model = Comment
        fields = "__all__"


class PostInfoSerializer(serializers.ModelSerializer):
    writer = UserInfoSerializer()
    comments = CommentInfoSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"
