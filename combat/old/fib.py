calls = 0

def fib(n):
    globals()['calls'] += 1
    if n<2: return n
    return fib(n-1) + fib(n-2)

fib(3)
print(calls)