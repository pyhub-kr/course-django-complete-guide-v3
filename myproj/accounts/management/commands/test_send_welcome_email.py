from django.core.management import BaseCommand

from accounts.models import User
from accounts.utils import send_welcome_email


class Command(BaseCommand):
    help = "지정 이메일 주소의 유저를 찾아서, 환영 이메일을 보냅니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "email", type=str, help="환영 이메일을 받은 유저의 이메일 주소"
        )

    def handle(self, *args, **options):
        email = options["email"]

        try:
            user = User.objects.get(email__iexact=email)
            send_welcome_email(user)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{email} 주소의 유저에게 환영 이메일을 발송했습니다."
                )
            )
        except User.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(f"{email} 주소를 유저를 찾을 수 없습니다.")
            )
