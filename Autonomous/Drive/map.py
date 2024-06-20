ranges = [
    (0, 1000, 5),
    (1000, 2000, 3), 
    (2000, 4000, 2),
    (4000, 5000, 1.5),
    (5000, 10000, 1),
    (10000, 20000, 0.75),
    (20000, 62000, 0.5)
]


def map(val, loval, hival, tolow, tohigh):
    return (val - loval) / (hival - loval) * (tohigh - tolow) + tolow

wm1 = int(map(-5, -255, 255, -62000, 62000))
wm2 = int(map(5, -255, 255, -62000, 62000))
wm3 = int(map(-5, -255, 255, -62000, 62000))
wm4 = int(map(5, -255, 255, -62000, 62000))
mul_fac = 1
print("Before Mapping")
print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))

for min_val, max_val, factor in ranges:
    if all(min_val <= abs(var) <= max_val for var in (wm1, wm2, wm3, wm4)):
        mul_fac = factor
        break

wm1 = int(mul_fac * wm1)
wm2 = int(mul_fac * wm2)
wm3 = int(mul_fac * wm3)
wm4 = int(mul_fac * wm4)
print("After Mapping")
print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
