import re
from io import BytesIO
from os.path import splitext
from typing import List
from uuid import uuid4

from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_str
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_UPDATE, AFTER_SAVE
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
        return reverse("photolog:note_detail", args=[self.pk])

    @hook(AFTER_SAVE, when="content", has_changed=True)
    def on_content_saved(self):
        hashtags: List[str] = re.findall(r"#(\w+)", self.content)
        self.tags.set(hashtags, clear=True)


def uuid_name_upload_to(instance: models.Model, filename: str) -> str:
    app_label = instance.__class__._meta.app_label
    cls_name = instance.__class__.__name__.lower()
    ymd_path = force_str(timezone.now().strftime("%Y/%m/%d"))
    extension = splitext(filename)[-1].lower()
    new_filename = uuid4().hex + extension
    return "/".join((app_label, cls_name, ymd_path, new_filename))


class Photo(LifecycleModelMixin, models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    image = models.ImageField(
        # upload_to="photolog/photo/%Y/%m/%d",
        upload_to=uuid_name_upload_to,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def make_thumb(
        cls, image_file: File, max_width: int = 1024, max_height: int = 1024, quality=80
    ) -> File:
        pil_image = Image.open(image_file)
        max_size = (max_width, max_height)
        pil_image.thumbnail(max_size)
        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGB")

        thumb_name = splitext(image_file.name)[0] + ".jpg"
        thumb_file = ContentFile(b"", name=thumb_name)
        pil_image.save(thumb_file, format="jpeg", quality=quality)

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

        cls.objects.bulk_create(photo_list)

        return photo_list

    @hook(BEFORE_UPDATE, when="image", has_changed=True)
    def on_image_changed(self):
        if self.image:
            image_width = self.image.width
            image_extension = splitext(self.image.name)[-1].lower()

            if image_width > 1024 or image_extension not in (".jpg", ".jpeg"):
                thumb_file = self.make_thumb(self.image.file, 1024, 1024, 80)
                self.image.save(thumb_file.name, thumb_file, save=False)


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-pk"]
