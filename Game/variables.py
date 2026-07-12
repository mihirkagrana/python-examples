# variables
user_input = input("Guess a number: ")
print("User Input:", user_input)

print(type(user_input))

user_input_int = int(user_input)

print(type(user_input_int))

# check memory address of variables. If variable value is same, address will also be same.
my_var = 2
print(id(my_var))
print(id(user_input_int))