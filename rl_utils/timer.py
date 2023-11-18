from functools import wraps
from time import perf_counter
from typing import Callable
from typing import Tuple


def timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        results = func(*args, **kwargs)
        end = perf_counter()
        run_time = end - start
        return results, run_time

    return wrapper


@timer
def predict_with_time(model, X_test: np.array) -> Tuple[np.array]:
    return model.predict(X_test)


@timer
def test(x):
    print(x)
    return x


x = test("hello world")

x
