# Generated by Django 4.2.6 on 2024-02-12 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(help_text="댓글 본문", max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Reply",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(help_text="대댓글 본문", max_length=100)),
                (
                    "comment",
                    models.ForeignKey(
                        help_text="댓글 id",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="boards.comment",
                    ),
                ),
                (
                    "writer",
                    models.ForeignKey(
                        help_text="작성자",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reply_writer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(help_text="제목", max_length=30)),
                ("content", models.TextField(help_text="게시글 본문", max_length=500)),
                ("view_count", models.IntegerField(default=0, help_text="조회수")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="작성일", null=True),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="업데이트일", null=True),
                ),
                (
                    "writer",
                    models.ForeignKey(
                        help_text="작성자",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="post_writer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                help_text="게시글 id",
                on_delete=django.db.models.deletion.CASCADE,
                to="boards.post",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="writer",
            field=models.ForeignKey(
                help_text="작성자",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comment_writer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
