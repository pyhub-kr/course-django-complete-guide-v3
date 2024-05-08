# core/pagination.py

import re
from typing import Type, cast, Literal
from rest_framework import pagination as drf_pagination


def make_pagination_class(
    cls_type: Literal["page_number", "limit_offset", "cursor"],
    page_size: int,
    max_limit: int = None,
    cursor_ordering: str = None,
) -> Type[drf_pagination.BasePagination]:
    base_cls_name = f"{cls_type.title().replace('_', '')}Pagination"
    base_cls = getattr(drf_pagination, base_cls_name)

    if cls_type == "page_number":
        cls_name = f"{base_cls_name}WithPageSize{page_size}"
        attrs = {"page_size": page_size}
    elif cls_type == "limit_offset":
        cls_name = f"{base_cls_name}WithDefaultLimit{page_size}AndMaxLimit{max_limit}"
        attrs = {"default_limit": page_size, "max_limit": max_limit}
    elif cls_type == "cursor":
        ordering = (cursor_ordering or "").title().replace("_", "")
        ordering = re.sub(r"^[+-]", "", ordering)
        cls_name = f"{base_cls_name}WithPageSize{page_size}AndOrdering{ordering}"
        attrs = {"page_size": page_size, "ordering": cursor_ordering}
    else:
        raise NotImplementedError(f"Not implemented cls_type : {cls_type}")

    cls = type(cls_name, (base_cls,), attrs)
    return cast(Type[drf_pagination.BasePagination], cls)
