#import library to generate random number

import random

users = {"user1", "user2", "user3"}
score_board = {"user1": 0, "user2": 0, "user3": 0}

round = 0
total_round = 5
while(round < total_round):
    random_number = random.randint(1,9)
    print("Random Number: ", random_number)
    # take input for every user
    for user in users:
        user_input = input(f"{user} Guess a number: ")
        user_input_int = int(user_input)

        print(user_input)

        if user_input_int == 0:
            print("Please add a non-zero number")
        else:
            if user_input_int == random_number:
                current_score = score_board.get(user)
                score_board[user] = current_score + 1
            pass
    round = round + 1

    print("Final Score: ", score_board)