# Classes and objects

# Encapsulation.
class Account:
    def __init__(self, balance=0):
        self.__balance = balance  # Private attribute

    def getBalance(self):
        print("Validating the user")
        return self.__balance

    def setBalance(self, balance):
        print("Validating the user")
        self.__balance = balance

myaccount = Account(500)
print(myaccount.getBalance())  # Output: 100
myaccount.setBalance(1000)
print(myaccount.getBalance())  # Output: 100

# Inheritance
class Animal:
    def __init__(self):
        pass
    
    def walk(self):
        print("Animal walks")

    def speak(self):
        print("Animal speaks")

    def eat(self):
        print("Animal eats")

class Cat(Animal):
    def speak(self):
        print("Cat meows")

    def eat(self):
        super().eat()  # Call the parent class's eat method
        print("Cat eats")

cat = Cat()
cat.walk()  # Output: Animal walks
cat.speak()  # Output: Cat meows
cat.eat()  # Output: Cat eats

# Kitten class
class Kitten(Cat):
    def eat(self):
        super().eat()  # Call the parent class's eat method
        print("Kitten eats")

k = Kitten()
k.eat()  # Output: Kitten eats