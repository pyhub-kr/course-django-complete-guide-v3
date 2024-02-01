# core/forms/renderers.py

from pathlib import Path
from django.conf import settings
from django.forms import renderers


class NoCacheDjangoTemplates(renderers.DjangoTemplates):
    if settings.DEBUG:
        # django 4.2 기준으로 작성된 코드
        # cached_property를 property로 변경
        # https://github.com/django/django/blob/4.2/django/forms/renderers.py#L36
        @property
        def engine(self):
            # django/forms/templates 경로
            form_templates_path = (
                Path(renderers.__file__).parent / self.backend.app_dirname
            )
            return self.backend(
                {
                    "APP_DIRS": True,
                    "DIRS": [form_templates_path],
                    "NAME": "djangoforms",
                    "OPTIONS": {},
                }
            )
