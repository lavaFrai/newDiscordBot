import math


def powTmp(a, b):
    if (-32569 <= a <= 32569) and (-32569 <= b <= 32569):
        return a ** b
    else:
        raise Exception("Для pow естановлены ограничения - 32569")


def factTmp(a):
    if -32569 <= a <= 32569:
        return math.factorial(a)
    else:
        raise Exception("Для fact естановлены ограничения - 32569")


def rangeTmp(a, b=None, c=None):
    if (-32569 <= a <= 32569) and (-32569 <= b <= 32569) and (-32569 <= c <= 32569):
        if b is None:
            return range(a)
        if c is None:
            return range(a, b)
        return range(a, b, c)
    else:
        raise Exception("Для range естановлены ограничения - 32569")


def sumTmp(a):
    if len(a) < 32569:
        if max(a) < 32569:
            return sum(a)
        else:
            raise Exception("Для sum естановлены ограничения максимума - 32569")
    else:
        raise Exception("Для sum естановлены ограничения длинны - 32569")


allowed_functions = {
    "range": rangeTmp,
    "list": list,
    "set": set,
    "str": str,
    "int": int,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos": lambda x: math.degrees(math.acos(x)),
    "atan": lambda x: math.degrees(math.atan(x)),
    "hypotenuse": math.hypot,
    "pow": powTmp,
    "pi": math.pi,
    "e": math.e,
    "deg": math.degrees,
    "rad": math.radians,
    "abs": abs,
    "fact": factTmp,
    "sum": sumTmp,
    "log": math.log,
    "sqrt": math.sqrt,
    "gamma": math.gamma
}


value = input()
try:
    result = eval(value, {'__builtins__': allowed_functions})
except BaseException as e:
    print("ERROR", end='\0')
    print(str(e), end='')
    exit(1)
print("OK", end='\0')
print(result, end='')
