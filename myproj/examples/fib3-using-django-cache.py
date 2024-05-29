# fib3-using-django-cache.py : 장고 캐시 API 활용

import time
from django.core.cache import caches

django_default_cache = caches["default"]

count = 0


def cache(func):
    def wrapper(n):
        key = n

        cached_result = django_default_cache.get(key)
        if cached_result is None:
            cached_result = func(n)
            django_default_cache.set(key, cached_result, timeout=60)

        return cached_result

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
