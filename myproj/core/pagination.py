# core/pagination.py

from typing import Type, cast, Literal
from rest_framework import pagination as drf_pagination


# 앞선 PageNumberPagination도 함께 지원
def make_pagination_class(
    cls_type: Literal["page_number", "limit_offset"],
    page_size: int,
    max_limit: int = None,
) -> Type[drf_pagination.BasePagination]:
    base_cls_name = f"{cls_type.title().replace('_', '')}Pagination"
    base_cls = getattr(drf_pagination, base_cls_name)

    if cls_type == "page_number":
        cls_name = f"{base_cls_name}WithPageSize{page_size}"
        attrs = {"page_size": page_size}
    elif cls_type == "limit_offset":
        cls_name = f"{base_cls_name}WithDefaultLimit{page_size}AndMaxLimit{max_limit}"
        attrs = {"default_limit": page_size, "max_limit": max_limit}
    else:
        raise NotImplementedError(f"Not implemented cls_type : {cls_type}")

    cls = type(cls_name, (base_cls,), attrs)
    return cast(Type[drf_pagination.BasePagination], cls)
