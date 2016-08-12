
def nothing(fn):
    def wrap():
        return fn()
    return wrap

def verbose(fn):
    def wrap(*args):
        print("함수호출 : {}".format(args))
        return fn(*args)
    return wrap

def absolute(fn):
    def wrap(x, y):
        return abs(fn(x, y))
    return wrap

@verbose
@absolute
def mysum(x, y):
    return x + y

print(mysum(1, -10))
