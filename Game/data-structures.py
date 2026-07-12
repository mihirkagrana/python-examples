# list, tuple, set and dict

# list
my_list = []
my_list.append(2)
my_list.append("Hello")
my_list.append(4.56)

my_list.insert(2, "Newly added string")

print(my_list)

my_list.pop(2)

print(my_list)

# tuple - is immutable
my_tuple = (1, "Hi", 4.1)
print(my_tuple[2])


# set - is mutable, but stores unique element. Set is unordered.
my_set = {1,2,3,4,4}
my_set.add("Hello")
my_set.discard(1)
print(my_set)

# dict - dictionary stores key and value
my_dict = {"key1":"value1", "key2":"value2", "key3":"value3"}
print(my_dict["key2"])

# data structures in our game
users = {"user1", "user2", "user3"}
score_board = {"user1": 0, "user2": 0, "user3": 0}

round = 0
total_round = 5
while(round < total_round):
    # take input for every user
    for user in users:
        user_input = input(f"{user} Guess a number: ")
        print(user_input)

        if int(user_input) == 0:
            print("Please add a non-zero number")
        else:
            pass
    round = round + 1