"""
Have a look at the script called 'human-guess-a-number.py' (in the same folder as this one).

Your task is to invert it: You should think of a number between 1 and 100, and the computer 
should be programmed to keep guessing at it until it finds the number you are thinking of.

At every step, add comments reflecting the logic of what the particular line of code is (supposed 
to be) doing. 
"""

from random import randint

def input_yes_no(prompt):
    # Asks the user for Yes/No input. If valid, the string input is returned as a boolean.
    response = input(prompt) # Asks the user for their response. Strips the input of whitespace and sets it to lowercase.
    while not check_str(response): # Repeats until the user input is valid.
        print('Please, enter a valid response.')
        response = input(prompt)
    return True if response.strip().lower() in ['yes', 'y'] else False # Returns True for a positive response and False for the negative.

def check_str(response):
    # Ensures yes/no input is readable as either 'Yes', 'Y', 'No' or 'N' and returns True. Otherwise, returns False to reject it.
    return True if response.strip().lower() in ['yes', 'y', 'no', 'n'] else False

def guess(lowerbound, upperbound):
    # Produces a guess within a given range and ask for user input on its correctness.
    n = randint(lowerbound, upperbound) # Generates a number within the provided range.
    if input_yes_no('Is your number ' + str(n) + '? '): # Asks the user to determine whether the guess is correct.
        return print('Success! Thanks for playing!') # Returns this final statement if the guess is correct.
    elif input_yes_no('Is it lower than ' + str(n) + '? '): # Asks the user to determine whether the guess is higher than the user's number.
        return guess(lowerbound, n) # The guess was too high: the function is returned with the guess as the upper bound.
    else:
        return guess(n, upperbound) # The guess was too low: the function is returned with the guess as the lower bound.

print('Think of a number between 1 and 100 and I will try to guess it!')
start = input_yes_no('Ready (Yes/No)? ')

if not start:
    print('Okay. Bye!') # Prints a closing statement if the user responds that they are not ready.
else:
    print('Answer "Yes" or "No" to the following questions.')
    guess(1, 100) # Starts guessing numbers recursively with an initial range of 1-100.