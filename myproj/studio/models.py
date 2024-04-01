import re
from os.path import normpath, splitext
from typing import List
from uuid import uuid4

from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_str
from django_lifecycle import hook, AFTER_SAVE, LifecycleModelMixin
from taggit.managers import TaggableManager

from accounts.models import User


class Note(LifecycleModelMixin, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self) -> str:
        return reverse("studio:note_detail", args=[self.pk])

    @hook(AFTER_SAVE, when="content", has_changed=True)
    def on_saved(self):
        hashtags: List[str] = re.findall(r"#(\w+)", self.content)
        self.tags.set(hashtags, clear=True)


def uuid_name_upload_to(instance: models.Model, filename: str) -> str:
    app_label = instance.__class__._meta.app_label
    cls_name = instance.__class__.__name__.lower()
    ymd_path = normpath(force_str(timezone.now().strftime("%Y/%m/%d")))
    extension = splitext(filename)[-1].lower()
    new_filename = uuid4().hex + extension
    return "/".join((app_label, cls_name, ymd_path, new_filename))


class Photo(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=uuid_name_upload_to,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def make_thumb(cls, file: File, max_width, max_height) -> File:
        pil_image = Image.open(file)
        pil_image.thumbnail((max_width, max_height))
        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGBA")

        thumb_name = splitext(file.name)[0] + ".jpg"
        thumb_file = ContentFile(b"", name=thumb_name)
        pil_image.save(thumb_file)

        return thumb_file

    @classmethod
    def create_photos(cls, note: Note, photo_file_list: List[File]) -> List["Photo"]:
        if not note.pk:
            raise ValueError("Note를 먼저 저장해주세요.")

        photo_list = []
        for photo_file in photo_file_list:
            photo = cls(note=note)
            photo.image.save(photo_file.name, photo_file, save=False)
            photo_list.append(photo)

        Photo.objects.bulk_create(photo_list)

        return photo_list
