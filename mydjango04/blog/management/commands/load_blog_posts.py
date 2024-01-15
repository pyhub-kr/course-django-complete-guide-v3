# blog/management/commands/load_blog_posts.py


from random import choice
import requests
from django.core.management import BaseCommand

from accounts.models import User
from blog.models import Category, Post, Tag, Comment


SAMPLE_POSTS_JSON_URL = (
    "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/sample-blog-post.json"
)

SAMPLE_COMMENTS_TXT_URL = (
    "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/sample-blog-comments.txt"
)


class Command(BaseCommand):
    help = "샘플 데이터로부터 블로그 애플리케이션에 데이터를 추가합니다."

    # 인자로 JSON 주소를 지정하지 않으면, 디폴트 주소를 활용
    def add_arguments(self, parser):
        parser.add_argument("posts_json_url", nargs="?", default=SAMPLE_POSTS_JSON_URL)
        parser.add_argument(
            "comments_txt_url", nargs="?", default=SAMPLE_COMMENTS_TXT_URL
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="새 데이터를 저장하기 전에 기존 데이터를 모두 삭제합니다.",
        )

    def handle(self, *args, **options):
        posts_json_url = options["posts_json_url"]
        comments_txt_url = options["comments_txt_url"]

        is_clear_data = options["clear"]

        if is_clear_data is True:
            clear_data()

        print("JSON/TXT 다운로드 중 ...")

        res = requests.get(posts_json_url)
        res.raise_for_status()
        orig_post_list = res.json()

        res = requests.get(comments_txt_url)
        res.raise_for_status()
        orig_comments_txt = res.text

        create_categories(orig_post_list)
        create_tags(orig_post_list)
        create_posts(orig_post_list)
        create_comments(orig_comments_txt)


def clear_data():
    print("카테고리 데이터 삭제 중 ...")
    Category.objects.all().delete()
    print("포스팅 데이터 삭제 중 ...")
    Post.objects.all().delete()
    print("태그 데이터 삭제 중 ...")
    Tag.objects.all().delete()


def create_categories(orig_post_list):
    """카테고리 생성"""

    existed_category_name_set = set(
        Category.objects.values_list("name", flat=True).distinct()
    )
    category_name_set = {orig_post["category_name"] for orig_post in orig_post_list}

    category_list = [
        Category(name=category_name)
        for category_name in category_name_set - existed_category_name_set
    ]

    if category_list:
        print(f"{len(category_list)} 개의 카테고리 생성")
        Category.objects.bulk_create(category_list, batch_size=1000)


def create_tags(orig_post_list):
    """태그 생성"""

    existed_tag_name_set = set(Tag.objects.values_list("name", flat=True).distinct())

    tag_name_set = set()
    for orig_post in orig_post_list:
        tag_name_set.update(orig_post["tag_list"])

    tag_list = [Tag(name=tag_name) for tag_name in tag_name_set - existed_tag_name_set]

    if tag_list:
        print(f"{len(tag_list)} 개의 태그 생성")
        Tag.objects.bulk_create(tag_list, batch_size=1000)


def create_posts(orig_post_list):
    """포스팅 생성"""

    category_dict = {category.name: category for category in Category.objects.all()}
    tag_dict = {tag.name: tag for tag in Tag.objects.all()}

    user_list = list(User.objects.all())

    post_list = []
    for orig_post in orig_post_list:
        post = Post(
            category=category_dict[orig_post["category_name"]],
            author=choice(user_list),
            title=orig_post["title"],
            status=choice([Post.Status.DRAFT, Post.Status.PUBLISHED]),
            content=orig_post["content"],
        )
        post._tag_list = orig_post["tag_list"]
        post.slugify()
        post_list.append(post)

    if post_list:
        print(f"{len(post_list)} 개의 포스팅 생성")
        Post.objects.bulk_create(post_list, batch_size=1000)

        for post in post_list:
            _tag_list = [tag_dict[tag_name] for tag_name in post._tag_list]
            post.tag_set.add(*_tag_list)


def create_comments(orig_comments_txt):
    user_list = list(User.objects.all())
    post_list = list(Post.objects.all())

    # 데이터 3배 뻥튀기
    lines = (
        orig_comments_txt + "\n" + orig_comments_txt + "\n" + orig_comments_txt
    ).splitlines()

    comment_list = []
    for message in lines:
        if message := message.strip():
            comment = Comment(
                author=choice(user_list), post=choice(post_list), message=message
            )
            comment_list.append(comment)

    if comment_list:
        print(f"{len(comment_list)} 개의 댓글 생성")
        Comment.objects.bulk_create(comment_list, batch_size=1000)
