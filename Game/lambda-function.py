# lambda arguments: expression

add = lambda x, y: x + y
print(add(5, 3))  # Output: 8

grade = lambda score: 'Pass' if score >= 50 else 'Fail'
print(grade(75))  # Output: Pass

multiply = lambda x: lambda y: x * y
double = multiply(2)
print(double(5))  # Output: 10