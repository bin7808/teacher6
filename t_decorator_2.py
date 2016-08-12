
def base(base_i):
    def wrap(fn):
        def inner(x, y):
            return base_i + abs(fn(x, y))
        return inner
    return wrap

@base(10)
def mysum(x, y):
    return x + y

print(mysum(1, 2))
