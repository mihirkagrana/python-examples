# Exception handling

a = 10
b = 0

try:
    c = a / b
    print("Last")
except Exception as e:
    print("Some exception")
    print(e)

finally:
    print("At last")