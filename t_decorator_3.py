
def alert(maximum):
    def wrap(fn):
        def inner(x, y):
            result = x + y
            if result > maximum:
                print('삐~삐~삐!!')
            return result
        return inner
    return wrap

@alert(10)
def mysum(x, y):
    return x + y

print(mysum(1, 9))
print(mysum(1, 10))

