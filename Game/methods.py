#import library to generate random number

import random

def generateRandomNumber():
    random_number = random.randint(1,9)
    return random_number

def verifyNumber(user_input, random_number):
    if user_input == 0:
        print("Please add a non-zero number")
    else:
        if user_input == random_number:
            current_score = score_board.get(user)
            score_board[user] = current_score + 1


users = {"user1", "user2", "user3"}
score_board = {"user1": 0, "user2": 0, "user3": 0}

round = 0
total_round = 5
while(round < total_round):
    random_number = generateRandomNumber()
    print("Random Number: ", random_number)
    # take input for every user
    for user in users:
        try:
            user_input = input(f"{user} Guess a number: ")
            user_input_int = int(user_input)
        except Exception as e:
            user_input = 10
            user_input_int = int(user_input)
        finally:
            print("Finally")

        print(user_input)
        verifyNumber(user_input_int, random_number)
    round = round + 1

    print("Final Score: ", score_board)