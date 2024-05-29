# fib1.py : 피보나치 수열의 35번째 값을 3번 계산한 경우

import time

count = 0


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
