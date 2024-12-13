# Tuple Out Dice Game
"""
This program simulates the "Tuple Out" dice game where players take turns rolling dice to score points.
The game continues until a player reaches the target score.
"""

import random  
import sys    
from collections import Counter 
import utils

# Rolls a specified number of dice and returns the results as a list
def roll_dice(num_dice=3):
    """
    Args:
        num_dice (int): Number of dice to roll. Default is 3.

    Returns:
        list: A list containing the results of the dice rolls.
    """
    return [random.randint(1, 6) for _ in range(num_dice)]

# Displays the current scores of all players
def display_scores(scores):
    """
    Args:
        scores (dict): A dictionary containing player names and their scores.
    """
    print("\nCurrent Scores:")
    for player, score in scores.items():
        print(player + ": " + str(score))

# Prompts the user to make a choice from the provided options
def get_user_choice(prompt, choices):
    """
    Args:
        prompt (str): The message displayed to the user.
        choices (list): A list of valid choices.

    Returns:
        str: The user's validated choice.
    """
    while True:
        choice = input(prompt).lower()  
        if choice in choices:
            return choice
        else:
            print("Invalid choice. Please choose from " + str(choices) + ".") 

# Executes a single turn for a player
def play_turn(player, scores, target_score):
    """
    Args:
        player (str): The name of the current player.
        scores (dict): The current scores of all players.
        target_score (int): The score needed to win the game.
    """
    print("\n" + player + "'s turn:") 
    fixed_dice = []
    total_points = 0

    while True:
        num_dice_to_roll = 3 - len(fixed_dice)
        current_roll = roll_dice(num_dice_to_roll)
        print(player + " rolled: " + str(current_roll + fixed_dice))  

        # Count occurrences of each die using Counter
        counts = Counter(current_roll + fixed_dice)

        # Check for tuples
        if any(count == 3 for count in counts.values()):
            print(player + " has tupled out! Scores 0 points this turn.")
            return

        # Fix dice with two of the same value
        new_fixed = [die for die, count in counts.items() if count == 2]
        if new_fixed:
            fixed_dice = new_fixed
            print("Fixed dice: " + str(fixed_dice)) 

        total_points = sum(current_roll) + sum(fixed_dice)
        print("Total points this turn: " + str(total_points)) 

        # Ask to continue or stop
        choice = get_user_choice("Do you want to (r)eroll or (s)top? ", ['r', 's'])
        if choice == 's':
            scores[player] += total_points
            print(player + " ends their turn with " + str(total_points) + " points.")  
            return

# The main function to run the Tuple Out Dice Game
def main():

    print("Welcome to the Tuple Out Dice Game!")

    # Setting target score 
    target_score = 50  # Default target score
    if len(sys.argv) > 1:
        target_score = int(sys.argv[1])
        print("Target score set to " + str(target_score) + " points.")  

    players = ["Player 1", "Player 2"]  
    scores = {player: 0 for player in players}  

    # Display scores of players at the end of each turn
    game_in_progress = True
    while game_in_progress:  
        for player in players:
            play_turn(player, scores, target_score)
            display_scores(scores)

            # Display final scores
            if scores[player] >= target_score:
                print("\n" + player + " has reached " + str(target_score) + " points and wins the game!")  
                utils.save_high_score(player, scores[player])  
                game_in_progress = False
                break

    # Using a tuple to display final scores
    final_scores = tuple(scores.items())
    print("\nFinal Scores:")
    for player, score in final_scores:
        print(player + ": " + str(score))  

    winner = max(scores, key=scores.get)
    print("\nCongratulations " + winner + "! You win the game.")
