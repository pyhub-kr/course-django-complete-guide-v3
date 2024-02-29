import random
import string

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


SESSIONS = {}


def session_get_or_create(request):
    global SESSIONS

    session_id = request.COOKIES.get("session_id", "")
    if session_id == "":
        sample = string.ascii_lowercase + string.digits
        while True:
            session_id = "".join(random.choice(sample) for __ in range(32))
            if session_id not in SESSIONS:
                break
        created = True
    else:
        created = False

    return session_id, created


@csrf_exempt
def coffee_stamp(request):
    global SESSIONS

    # SESSIONS 전역변수에 session_id가 등록되어있지 않다면, 생성
    session_id, session_created = session_get_or_create(request)
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {"phone": "", "order_count": 0}
    session = SESSIONS[session_id]

    if request.method == "GET":
        response = HttpResponse(
            """
            <form method="POST">
                <input type="text" name="phone" placeholder="적립을 위해 휴대폰 번호를 입력해주세요." />
            </form>
            """
        )
    else:
        phone = request.POST["phone"]
        order_count = session.get(phone, 0)
        order_count += 1
        session[phone] = order_count

        response = HttpResponse(
            f"""
            {phone}님. 적립횟수 : {order_count}<br/>
            10회 이상 스탬프를 찍으셨다면
            <a href="/cafe/free-coffee/">무료커피를 신청해주세요.</a>
            """
        )

    if session_created:
        response.set_cookie("session_id", session_id)

    return response


def coffee_free(request):
    global SESSIONS

    # SESSIONS 전역변수에 session_id가 등록되어있지 않다면, 생성
    session_id, session_created = session_get_or_create(request)
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {"phone": "", "order_count": 0}
    session = SESSIONS[session_id]

    phone = session.get("phone", "")
    if not phone:
        return redirect("cafe:coffee_stamp")

    order_count = session.get("order_count", 0)
    if order_count < 10:
        response = HttpResponse(
            f"{phone}님. 스탬프 {order_count}번 찍으셨어요. {10-order_count}번 찍으시면 무료쿠폰을 받을 수 있습니다."
        )
    else:
        response = HttpResponse(f"{phone}님. 무료쿠폰을 사용하시겠어요?")

    if session_created:
        response.set_cookie("session_id", session_id)

    return response
