# Loops and Conditions

round = 0
total_round = 5
while(round < total_round):
    user_input = input("Guess a number: ")
    print(user_input)

    if int(user_input) == 0:
        print("Please add a non-zero number")
    else:
        pass
        round = round + 1