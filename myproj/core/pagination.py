from typing import Type, cast

from rest_framework.pagination import BasePagination, PageNumberPagination


def make_pagination_class(
    page_size: int,
) -> Type[BasePagination]:
    cls_name = f"PageNumberPaginationWithPageSize{page_size}"
    base_cls = PageNumberPagination
    attrs = {"page_size": page_size}

    cls = type(cls_name, (base_cls,), attrs)
    return cast(Type[BasePagination], cls)
