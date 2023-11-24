# core/context_processors.py

from django.contrib import messages


def lazy_messages_list(request):
    # 장고 템플릿에서는 인자없는 함수를 호출할 수 있습니다.
    # 아래 messages_list 함수에서 사전을 만들 때
    # 메시지 목록을 가져오는 것이 아니라,
    # 메시지를 소비하는 시점에 메시지를 가져오도록 지연시킵니다.
    def inner():
        message_list = messages.get_messages(request)

        # 변환이 가능한 타입인 리스트와 사전으로 먼저 변환
        return [
            {
                "level_tag": message.level_tag,
                "message": message.message,
            }
            for message in message_list
        ]

    return inner


def messages_list(request):
    return {
        "messages_list": lazy_messages_list(request),
    }
