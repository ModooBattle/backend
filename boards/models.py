from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30, blank=False, null=False, help_text="제목")
    content = models.TextField(max_length=500, blank=False, null=False, help_text="게시글 본문")
    writer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="post_writer", blank=True, null=False, help_text="작성자"
    )
    category = models.ForeignKey(
        "sports.Sport",
        on_delete=models.CASCADE,
        related_name="post_category",
        blank=True,
        null=False,
        help_text="종목id",
    )
    like_count = models.IntegerField(blank=False, null=False, default=0, help_text="좋아요 수")
    view_count = models.IntegerField(blank=False, null=False, default=0, help_text="조회수")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, help_text="업데이트일")


class Comment(models.Model):
    writer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="comment_writer", blank=False, null=False, help_text="작성자"
    )
    post = models.ForeignKey(
        "boards.Post", related_name="comments", on_delete=models.CASCADE, blank=False, null=False, help_text="게시글 id"
    )
    content = models.TextField(max_length=100, help_text="댓글 본문")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, help_text="업데이트일")


class Reply(models.Model):
    writer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reply_writer", blank=False, null=False, help_text="작성자"
    )
    comment = models.ForeignKey(
        "boards.Comment", on_delete=models.CASCADE, related_name="replies", blank=False, null=False, help_text="댓글 id"
    )
    content = models.TextField(max_length=100, help_text="대댓글 본문")
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True, help_text="업데이트일")
