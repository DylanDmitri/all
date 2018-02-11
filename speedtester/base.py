import time

def inlineIf(val, flip):
    return (-val if flip else val)

def implicitIf(val, flip):
    return (val, -val)[flip]

def compare(implementations, params):
    for func in implementations:
        start = time.process_time()

        for param in params:
            func(*param)

        end = time.process_time()
        yield end-start

f1 = []
f2 = []
for trial in range(100):
    res = compare(
        (inlineIf, implicitIf),
        tuple((i, b) for i in range(5000000) for b in (True, False)))
