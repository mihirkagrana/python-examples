def calnumGenerator(num):
    for x in range(num):
        val = x * x
        yield val

val = calnumGenerator(10000)
for v in val:
    print(v)

#print(next(val))
#print(next(val))
#print(next(val))