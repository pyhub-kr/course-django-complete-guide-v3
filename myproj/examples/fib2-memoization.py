# fib2-memoization.py : 메모리에 저장

import time

count = 0


def cache(func):
    cached = {}  # 메모리에 캐싱 결과 저장

    def wrapper(n):
        key = n
        if key not in cached:
            cached[key] = func(n)
        return cached[key]

    return wrapper


@cache
def fib(n):
    global count
    count += 1

    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


for __ in range(3):
    start_time = time.time()
    count = 0
    result = fib(35)
    elapsed_time = time.time() - start_time
    print(
        f"반환값: {result}, " f"수행시간: {elapsed_time:.1f} 초, " f"호출횟수: {count}"
    )
