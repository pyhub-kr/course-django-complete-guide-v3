from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


ORDER_COUNTS = {}


@csrf_exempt
def coffee_stamp(request):
    global ORDER_COUNTS

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
        order_count = ORDER_COUNTS.get(phone, 0)
        order_count += 1
        ORDER_COUNTS[phone] = order_count

        response = HttpResponse(
            f"""
            {phone}님. 적립횟수 : {order_count}<br/>
            10회 이상 스탬프를 찍으셨다면
            <a href="/cafe/free-coffee/">무료커피를 신청해주세요.</a>
            """
        )
        response.set_cookie("phone", phone)

    return response


def coffee_free(request):
    phone = request.COOKIES.get("phone", "")
    if not phone:
        return redirect("cafe:coffee_stamp")

    order_count = ORDER_COUNTS.get(phone, 0)
    if order_count < 10:
        return HttpResponse(
            f"{phone}님. 스탬프 {order_count}번 찍으셨어요. {10-order_count}번 찍으시면 무료쿠폰을 받을 수 있습니다."
        )
    else:
        return HttpResponse(f"{phone}님. 무료쿠폰을 사용하시겠어요?")
