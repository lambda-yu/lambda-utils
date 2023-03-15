from typing import Callable
from functools import wraps

"""
将一个 函数 装饰为 装饰器 的装饰器~！
"""


class Func:
    def __init__(self, func, args, kwargs):
        self.__args = args
        self.__kwargs = kwargs
        self.__func: Callable = func

    def __call__(self):
        return self.__func(*self.__args, **self.__kwargs)

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return self.__kwargs

    @property
    def func(self) -> Callable:
        return self.__func


def wrap_parameter(decorator_func: Callable):
    @wraps(decorator_func)
    def parameter(*de_args, **de_kwargs):
        def inner(call_func: Callable):
            @wraps(call_func)
            def i_inner(*args_i, **kwargs_i):
                func = Func(call_func, args_i, kwargs_i)

                decorator_func(func, *de_args, **de_kwargs)
                return decorator_func

            return i_inner

        return inner

    return parameter


def wrap(decorator_func: Callable):
    @wraps(decorator_func)
    def inner(call_func: Callable):
        @wraps(call_func)
        def i_inner(*args_i, **kwargs_i):
            func = Func(call_func, args_i, kwargs_i)
            decorator_func(func)
            return decorator_func

        return i_inner

    return inner


# 我想写一个装饰器，但是我比较懒，于是用一个装饰器把函数装饰为装饰器，达到了写一个装饰器一样的效果~！
# 这是一个不带参装饰器
@wrap
def dog_bark(func):
    print("eat before wang~!")
    result = func()
    print(func.args, func.kwargs)
    print(func.func)
    print("eat after wang~!")
    return result


# 这是一个带参装饰器
@wrap_parameter
def dog_bark_p(func, a, b):
    print(f"eat before {'wang~! ' * a}")
    result = func()
    print(func.args, func.kwargs) # 获得被装饰函数的参数列表
    print(func.func)
    print(f"eat before {'wang~! ' * b}")
    return result


# 这是使用一个不带参装饰器
@dog_bark
def dog_eat(a):
    [print(f"dog eat hot dog {i}~!") for i in range(a)]


# 这是使用一个带参装饰器
@dog_bark_p(b=5, a=3)
def dog_eat_p(a):
    [print(f"dog eat hot dog {i}~!") for i in range(a)]


if __name__ == '__main__':
    dog_eat(2)
    dog_eat_p(a=3)
