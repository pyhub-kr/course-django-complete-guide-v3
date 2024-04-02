from django import template
import uuid

register = template.Library()


@register.simple_tag
def generate_uuid4(prefix=None, length=None) -> str:
    uuid4_hex = uuid.uuid4().hex
    if length:
        uuid4_hex = uuid4_hex[:length]
    return (prefix or "") + uuid4_hex
