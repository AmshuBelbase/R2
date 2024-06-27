ranges = [
    (0,250, 20),
    (0,500, 15),
    (0, 1000, 8),
    (0, 2000, 5), 
    (0, 4000, 2),
    (0, 5000, 1.2)
]


def map(val, loval, hival, tolow, tohigh):
    return (val - loval) / (hival - loval) * (tohigh - tolow) + tolow

wm1 = int(map(-6, -255, 255, -62000, 62000))
wm2 = int(map(6, -255, 255, -62000, 62000))
wm3 = int(map(-6, -255, 255, -62000, 62000))
wm4 = int(map(6, -255, 255, -62000, 62000))
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