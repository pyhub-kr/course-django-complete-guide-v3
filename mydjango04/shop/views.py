from django.http import HttpResponse


def current_travel_edit(request):
    """
    로그인 상황이라면, 여행의 출발지/도착지를 변경합니다.
    """

    if not request.user.is_authenticated:  # 로그인 여부
        return HttpResponse("Unauthorized", status=401)

    src = request.GET.get("src")  # 여행 출발지
    dest = request.GET.get("dest")  # 여행 도착지

    # 최근 여행의 출발지/도착지를 변경합니다.
    message = f"{request.user}의 여행지를 {src}/{dest}로 변경했습니다."
    print(message)

    return HttpResponse(message)
