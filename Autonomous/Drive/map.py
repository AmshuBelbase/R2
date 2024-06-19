ranges = [
    (-1000, 1000, 7),
    (-2000, 2000, 4), 
    (-5000, 5000, 2),
    (-10000, 10000, 1)
]

def map(val, loval, hival, tolow, tohigh):
    return (val - loval) / (hival - loval) * (tohigh - tolow) + tolow

wm1 = int(map(4, -255, 255, -62000, 62000))
wm2 = int(map(75, -255, 255, -62000, 62000))
wm3 = int(map(4, -255, 255, -62000, 62000))
wm4 = int(map(4, -255, 255, -62000, 62000))
mul_fac = 0.5
print("Before Mapping")
print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))

for min_val, max_val, factor in ranges:
    if all(min_val <= var <= max_val for var in (wm1, wm2, wm3, wm4)):
        mul_fac = factor
        break

wm1 *= mul_fac
wm2 *= mul_fac
wm3 *= mul_fac
wm4 *= mul_fac
print("After Mapping")
print("W1: {}, W2: {}, W3: {}, W4: {}".format(wm1,wm2,wm3,wm4))
