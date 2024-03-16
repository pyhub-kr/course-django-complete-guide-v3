# blog/management/commands/load_blog_tags.py

import requests  # pip install requests
from django.core.management import BaseCommand

from blog.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        txt_url = (
            "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/tags-example.txt"
        )

        txt = requests.get(txt_url).text
        tag_set = {line.strip() for line in txt.splitlines()}

        existed_tag_set = set(Tag.objects.all().values_list("name", flat=True))
        making_tag_set = tag_set - existed_tag_set

        tag_list = [Tag(name=tag_name) for tag_name in making_tag_set]
        created_tag_list = Tag.objects.bulk_create(tag_list)
        self.stdout.write(f"{len(created_tag_list)} tags created")
