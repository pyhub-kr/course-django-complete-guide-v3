import ipaddress
from typing import Union, Optional

from django.core.exceptions import ValidationError
from django.db import models


class BooleanYNField(models.BooleanField):
    true_value = "Y"
    false_value = "N"

    default_error_messages = {
        # null=False 일 때의 값 오류 메시지
        "invalid": (
            f"“%(value)s” 값은 True/False 값이어야 하며 "
            f"'{true_value}'/'{false_value}' 문자열도 지원합니다."
        ),
        # null=True 일 때의 값 오류 메시지
        "invalid_nullable": (
            f"“%(value)s” 값은 None이거나 True/False 값이어야 하며 "
            f"'{true_value}'/'{false_value}' 문자열도 지원합니다."
        ),
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 1)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def to_python(self, value: Union[str, bool]) -> Optional[bool]:
        if self.null and value in self.empty_values:
            return None

        if value == self.true_value:
            return True
        if value == self.false_value:
            return False

        return super().to_python(value)

    def from_db_value(
        self, value: Optional[str], expression, connection
    ) -> Optional[bool]:
        return self.to_python(value)

    def get_prep_value(self, value: Union[str, bool]) -> Optional[str]:
        prep_value: Optional[bool] = super().get_prep_value(value)
        if prep_value is None:
            return None
        return self.true_value if prep_value else self.false_value


class IPv4AddressIntegerField(models.CharField):
    default_error_messages = {
        "invalid": "“%(value)s” 값은 IPv4 주소나 정수여야 합니다.",
        "invalid_nullable": "“%(value)s” 값은 None이거나 IPv4 주소나 정수여야 합니다.",
    }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 15)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "PositiveIntegerField"

    def db_type(self, connection):
        if connection.vendor == "postgresql":
            return "bigint"
        if connection.vendor == "oracle":
            return "number(19)"
        return super().db_type(connection)

    def to_python(self, value: Union[str, int]) -> Optional[str]:
        if self.null and value in self.empty_values:
            return None

        if isinstance(value, str) and value.isdigit():
            value = int(value)

        try:
            return str(ipaddress.IPv4Address(value))
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            raise ValidationError(
                self.default_error_messages[
                    "invalid_nullable" if self.null else "invalid"
                ],
                code="invalid",
                params={"value": value},
            )

    def from_db_value(self, value: Optional[int], expression, connection) -> str:
        return self.to_python(value)

    def get_prep_value(self, value: Union[str, int]) -> Optional[int]:
        prep_value: Optional[str] = super().get_prep_value(value)
        if prep_value is None:
            return None
        return int(ipaddress.IPv4Address(prep_value))
