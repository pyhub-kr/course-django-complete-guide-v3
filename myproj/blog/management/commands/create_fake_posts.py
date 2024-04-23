# blog/management/commands/create_fake_posts.py

import random
from faker import Faker
from tqdm import tqdm

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from blog.models import Post, Comment


fake = Faker(locale="ko_KR")
User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_list = []
        post_list = []
        comment_list = []

        for __ in tqdm(range(10), desc="유저 생성"):
            username = fake.email().split("@")[0]
            password = (
                username  # 이후 API 테스트할 때, 인증을 위해 유저명으로 암호 설정
            )
            user = User.objects.create_user(username=username, password=password)
            user_list.append(user)

        for __ in tqdm(range(100), desc="포스팅 생성"):
            author = random.choice(user_list)
            title = fake.sentence(nb_words=6, variable_nb_words=True)[
                :100
            ]  # 짧은 텍스트
            content = fake.paragraph(
                nb_sentences=5, variable_nb_sentences=True
            )  # 긴 텍스트
            post = Post(
                author=author,
                title=title,
                content=content,
            )
            post_list.append(post)

        print(f"{len(post_list)}개의 포스팅 저장 중 ...")
        Post.objects.bulk_create(post_list)

        # 댓글 생성

        for __ in tqdm(range(10000), desc="댓글 생성"):
            post = random.choice(post_list)
            message = fake.sentence(nb_words=10, variable_nb_words=True)
            comment = Comment(
                post=post,
                message=message,
            )
            comment_list.append(comment)

        print(f"{len(comment_list)}개의 댓글 저장 중 ...")
        Comment.objects.bulk_create(comment_list)
