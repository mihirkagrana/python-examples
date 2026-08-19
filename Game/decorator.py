import random

def randomNumberGenerator(func):
    def wrapper():
        random_number = random.randint(100, 1000)
        func(random_number)
    return wrapper

@randomNumberGenerator
def functionA(num):
    print(f"Random number for function A: {num}")

@randomNumberGenerator
def functionB(num):
    print(f"Random number for function B: {num}")

@randomNumberGenerator
def functionC(num):
    print(f"Random number for function C: {num}")

functionA()
functionB()
functionC()