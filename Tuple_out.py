# Tuple Out Dice Game
"""
This program simulates the "Tuple Out" dice game where players take turns rolling dice to score points.
The game continues until a player reaches the target score.
"""
import random
import sys
from collections import Counter

def roll_dice(num_dice=3):
    """
    Rolls a specified number of dice and returns the results as a list.

    Args:
        num_dice (int): Number of dice to roll. Default is 3.

    Returns:
        list: A list containing the results of the dice rolls.
    """
    return [random.randint(1, 6) for _ in range(num_dice)]

def display_scores(scores):
    """
    Displays the current scores of all players.

    Args:
        scores (dict): A dictionary containing player names and their scores.
    """
    print("\nCurrent Scores:")
    for player, score in scores.items():
        print(player + ": " + str(score))

def tuple_out_check(counts):
    """
    Checks if a player has rolled a tuple (three of the same value).

    Args:
        counts (Counter): A Counter object containing the frequency of each die value.

    Returns:
        bool: True if a tuple (three of the same die) is rolled, otherwise False.
    """
    return any(count == 3 for count in counts.values())

def get_fixed_dice(counts):
    """
    Retrieves dice that are fixed (two of the same value).
    Args:
        counts (Counter): A Counter object containing the frequency of each die value.

    Returns:
        list: A list of dice with two of the same value.
    """
    return [die for die, count in counts.items() if count == 2]

def play_turn(player, scores, target_score):
    """
    Executes a single turn for a player.

    Args:
        player (str): The name of the current player.
        scores (dict): The current scores of all players.
        target_score (int): The score needed to win the game.

    Returns:
        int: The points scored during the player's turn.
    """
    print("\n" + player + "'s turn:")
    fixed_dice = []
    total_points = 0

    while True:
        num_dice_to_roll = 3 - len(fixed_dice)  # Determine how many dice to roll
        current_roll = roll_dice(num_dice_to_roll)
        print(player + " rolled: " + str(current_roll + fixed_dice))

        # Count occurrences of each die using Counter
        counts = Counter(current_roll + fixed_dice)

        if tuple_out_check(counts):
            print(player + " has tupled out! Scores 0 points this turn.")
            return 0

        # Fix dice with two of the same value
        new_fixed = get_fixed_dice(counts)
        if new_fixed:
            fixed_dice = new_fixed
            print("Fixed dice: " + str(fixed_dice))

        total_points = sum(current_roll) + sum(fixed_dice)
        print("Total points this turn: " + str(total_points))

        scores[player] += total_points
        print(player + " ends their turn with " + str(total_points) + " points.")
        return total_points

def main():
    print("Welcome to the Tuple Out Dice Game!")

    # Parse command-line arguments for target score
    target_score = 50  # Default target score
    if len(sys.argv) > 1:
        target_score = int(sys.argv[1])
        print("Target score set to " + str(target_score) + " points.")

    players = ["Player 1", "Player 2"]
    scores = {player: 0 for player in players}

    # Game loop
    game_in_progress = True
    while game_in_progress:
        player_index = 0  # Start with the first player
        while player_index < len(players):
            player = players[player_index]
            turn_points = play_turn(player, scores, target_score)
            if turn_points == 0:  # If a player tupled out, they score 0 for that turn
                player_index += 1
                continue

            display_scores(scores)

            if scores[player] >= target_score:
                print("\n" + player + " has reached " + str(target_score) + " points and wins the game!")
                print("Final Scores:")
                for player, score in scores.items():
                    print(player + ": " + str(score))
                game_in_progress = False
                break
            player_index += 1

if __name__ == "__main__":
    main()
