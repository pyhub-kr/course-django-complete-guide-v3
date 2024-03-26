from django.core.management import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "이메일 주소의 사용자를 찾아서 환영 이메일을 보냅니다."

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="환영 이메일을 받을 사용자 이메일")

    def handle(self, *args, **options):
        email = options["email"]
        try:
            user = User.objects.get(email=email)
            user.send_welcome_email()
            self.stdout.write(
                self.style.SUCCESS(f"{email}에게 성공적으로 환영 이메일을 보냈습니다")
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"{email} 이메일을 가진 사용자가 존재하지 않습니다")
            )
