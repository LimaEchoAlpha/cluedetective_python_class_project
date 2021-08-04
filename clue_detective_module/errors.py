"""This module contains helper functions for detecting errors in the user input from prompts."""

from board import *
from sys import exit

def is_valid_player(user_input):
    """This function determines if the user input is a valid player.
       If input is 'Q', exits program.
       
       Args: user input
       Returns: True or False
    """
    
    i = user_input.upper()
    if i in Board.player_decoder:
        return True
    elif i == 'Q':
        exit("\nExiting program. Thanks for using Clue Detective!\n")
    else:
        return False

def is_valid(user_input, card_type=None, skip=False):
    """This function determines if the user input is a valid card.
       If skip = True, also allows 'X' as a valid input.
       If input is 'Q', exits program.
       
       Args: user input
       Returns: True or False
    """
    
    i = user_input.upper()
    if i == 'Q':
        exit("\nExiting program. Thanks for using Clue Detective!\n")
    if skip:
        if i == 'X':
            return True
    if card_type:
        key_list = [key for key in Board.input_decoder 
                    if Board.input_decoder[key].type == card_type]
        if i in key_list:
            return True
    elif not card_type:
        if i in Board.input_decoder:
            return True      
    else:
        return False

def collect_players_and_suspects_list():
    """This function collects a list user inputs for players
       and suspects and decodes them.
       
       Args: none
       Returns: list of players decoded from valid user inputs
    """
    
    players_list = []
    while (players_input := input("Enter player: ")) != '#':
        i = players_input.upper()
        if not is_valid_player(i):
            print("Please enter a valid Suspect.")
            continue
        if i not in players_list:
            players_list.append(i)
    players_decoded = [Board.identify(player) for player in players_list]
    suspects_decoded = [Board.translate(player) for player in players_list]
    return players_decoded, suspects_decoded

def collect_players_list():
    """This function collects a list user inputs for players and decodes them.
       
       Args: none
       Returns: list of players decoded from valid user inputs
    """
    
    players_list = []
    while (players_input := input("Enter player: ")) != '#':
        i = players_input.upper()
        if not is_valid_player(i):
            print("Please enter a valid Suspect.")
            continue
        if i not in players_list:
            players_list.append(i)
    players_decoded = [Board.identify(player) for player in players_list]
    suspects_decoded = [Board.translate(player) for player in players_list]
    return players_decoded

def collect_cards():
    """This function collects a list user inputs for cards and decodes them.
       
       Args: none
       Returns: list of cards decoded from valid user inputs
    """
    
    cards_list = []
    while (cards_input := input("Enter card: ")) != '#':
        i = cards_input.upper()
        if not is_valid(i):
            print(f"Please enter a valid card.")
            continue
        cards_list.append(i)
    cards_decoded = [Board.translate(card) for card in cards_list]
    return cards_decoded
