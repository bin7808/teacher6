import time

def memoize(fn):
    cached = {}
    def wrap(x, y):
        key = (x, y)
        if key not in cached:
            cached[key] = fn(x, y)
        return cached[key]
    return wrap


@memoize
def mysum(x, y):
    time.sleep(1)
    return x + y

@memoize
def mymultiply(x, y):
    time.sleep(1)
    return x * y

print(mysum(1, 2))
print(mysum(2, 3))
print(mysum(1, 2))
print(mysum(1, 2))

print(mymultiply(1, 2))
print(mymultiply(10, 2))
print(mymultiply(1, 2))
print(mymultiply(1, 2))