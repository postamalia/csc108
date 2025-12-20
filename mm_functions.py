"""CSC108H1: Fall 2025 -- Assignment 1: Mystery Message Functions

Instructions (READ THIS FIRST!)
===============================

Make sure that the files a1_checker.py, a1_pyta.json, checker_generic.py
and mystery_message_game.py are in the same folder as this file
(mm_functions.py).

Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students 
taking the CSC108H1 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 CSC108H1 Teaching Team
"""

# points earned on each occurrence of a correctly guessed consonant
CONSONANT_POINTS = 1

# cost of buying a vowel, does not depend on the number of occurrences
VOWEL_COST = 1

# points earned on each occurrence of hidden consonants at the time of
# solving the puzzle
CONSONANT_BONUS = 2

# players' names
PLAYER_ONE = 'Player One'
PLAYER_TWO = 'Player Two'

# menu options
CONSONANT = 'C'  # guess a consonant
VOWEL = 'V'      # buy a vowel
SOLVE = 'S'      # try to solve the puzzle
QUIT = 'Q'       # quit the game

# symbol used for hidden characters
HIDDEN = '^'

# Game types
HUMAN = 'P1'             # one player, human
HUMAN_HUMAN = 'PVP'      # two players, human+human (player vs player)
HUMAN_COMPUTER = 'PVE'   # two players, human+computer (player vs environment)

# computer difficulty levels
EASY = 'E'  # computer plays the "easy" strategy
HARD = 'H'  # computer plays the "hard" strategy

# all consonants and all vowels
ALL_CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
ALL_VOWELS = 'aeiou'

# the order in which a computer player, hard difficulty level, will
# guess consonants
PRIORITY_CONSONANTS = 'tnrslhdcmpfygbwvkqxjz'


# We provide this function as an example.
# This function is already complete. You must not modify it.
def is_win(view: str, message: str) -> bool:
    """Return True if and only if message and view are a winning
    combination. That is, if and only if message and view are the same.

    >>> is_win('banana', 'banana')
    True
    >>> is_win('a^^le', 'apple')
    False
    >>> is_win('app', 'apple')
    False
    """

    return message == view


# We provide this function as an example of using a function as a helper.
# This function is already complete. You must not modify it.
def is_game_over(view: str, message: str, move: str) -> bool:
    """Return True if and only if message and view are a winning
    combination or move is QUIT.

    >>> is_game_over('a^^le', 'apple', VOWEL)
    False
    >>> is_game_over('a^^le', 'apple', 'Q')
    True
    >>> is_game_over('apple', 'apple', 'S')
    True
    """

    return move == QUIT or is_win(view, message)


# Helper function for computer_chooses_solve
# This function is already complete. You must not modify it.
def half_revealed(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic
    characters in view are revealed.

    >>> half_revealed('')
    True
    >>> half_revealed('x')
    True
    >>> half_revealed('^')
    False
    >>> half_revealed('a^,^c!')
    True
    >>> half_revealed('a^b^^e ^c^d^^d')
    False
    """

    num_hidden = view.count(HIDDEN)
    num_alphabetic = 0
    for char in view:
        if char.isalpha():
            num_alphabetic = num_alphabetic + 1
    return num_alphabetic >= num_hidden


# Implement the required functions below.
#
# We have provided the complete docstring (but not the body!) for the first
# function you are to write.  Write a function body for the function
# is_human.
#
# The header and docstring of is_human is an example of where and how to use
# constants in the docstring. We use the default values of constants in
# the docstring examples, but must use the constants in the function body.
    
def is_human(current_player: str, game_type: str) -> bool:
    """Return True if and only if current_player represents a human in a
    game of type game_type.

    current_player is PLAYER_ONE or PLAYER_TWO.
    game_type is HUMAN, HUMAN_HUMAN, or HUMAN_COMPUTER.

    In a HUMAN game or a HUMAN_HUMAN game, a player is always
    human. In a HUMAN_COMPUTER game, PLAYER_ONE is human and
    PLAYER_TWO is computer.

    >>> is_human('Player One', 'P1')
    True
    >>> is_human('Player One', 'PVP')
    True
    >>> is_human('Player Two', 'PVP')
    True
    >>> is_human('Player One', 'PVE')
    True
    >>> is_human('Player Two', 'PVE')
    False
    """

    # Complete the body of this function.
    return game_type == 'PVP' or game_type == 'P1' or (game_type == 'PVE' and
                                                       current_player ==
                                                       'Player One')

# Now define the other functions described in the handout.
# Follow the Function Design Recipe to produce complete functions for
# is_one_player_game, current_player_score, is_bonus_letter, 
# get_updated_char_view, calculate_score, next_player, is_fully_hidden,
# computer_chooses_solve, and remove_at_index.

def is_one_player_game(current_game: str) -> bool:
    """Return True if and only if current_game is a one-player game.
    
    >>> current_game('P1')
    True
    >>> current_game('PVE')
    False
    >>> current_game('PVP)
    False
    """
   
    return current_game == 'P1'
    
def current_player_score(player_one_score: int, player_two_score: int, 
                         current_player: str) -> int:
    """Return the score of current_player,
    given current_player, player_one_score and player_two_score.
    
    >>> current_player_score(2, 3, 'Player One')
    2
    >>> current_player_score(2, 3, 'Player Two')
    3
    """
  
    if current_player == PLAYER_ONE:
        return player_one_score
    else:
        return player_two_score
    
def is_bonus_letter(current_view: str, letter: str, 
                    mystery_message: str) -> bool:
    """Return True if and only if letter is a bonus letter.
   
    Bonus letters are consonants occurring in mystery_message and HIDDEN
    in current_view.
    
    >>> is_bonus_letter('a^^le', 'p', 'apple')
    True
    >>> is_bonus_letter('^arl gr^y', 'e', 'earl grey')
    False
    >>> is_bonus_letter('^anana', 'n', 'banana')
    False
    """
  
    return (letter in ALL_CONSONANTS and letter in mystery_message 
            and not letter in current_view)
    
def get_updated_char_view(current_view: str, mystery_message: str, 
                          character_index: int, character_guess: str) -> str:
    """Return the updated view of the character at character_index as a 
    single character string.
            
    If character_guess is correct (occurring at character_index in 
    mystery_message and hidden in current_view), the character is returned. 
    Otherwise, the character occurring at character_index in current_view
    is returned unchanged.
    
    Precondition: 0 <= character_index <= (len(mystery_message) - 1)

    >>> get_updated_char_view('^^^le', 'apple', 0, 'a')
    'a'
    >>> get_updated_char_view('e^rl gr^y', 'earl grey', 1, 'e')
    '^'
    >>> get_updated_char_view('ba^a^a', 'banana', 2, 'n')
    'n'
    """    
    
    if (character_guess == mystery_message[character_index] and 
        current_view[character_index] == HIDDEN):
        return mystery_message[character_index]
    else:
        return current_view[character_index]
    
def calculate_score(current_score: int, occurrences_revealed: int, 
                    current_move: str) -> int:
    """Return the updated score after current_move, given
    the current_score and the number of occurrences_revealed.
    
    Guessing a vowel costs VOWEL_COST, regardless of the number of
    occurrences_revealed. Guessing a consonant costs no points, and wins
    CONSONANT_POINTS for every 1 occurrences_revealed.
    
    Precondition: current_move == 'V' or current_move == 'C' 
    
    >>> calculate_score(6, 2, 'V')
    5
    >>> calculate_score(6, 0, 'V')
    5
    >>> calculate_score(2, 3, 'C')
    5
    """
    
    if current_move == VOWEL:
        return current_score - VOWEL_COST
    else:
        return current_score + (CONSONANT_POINTS * occurrences_revealed) 

def next_player(current_player: str, occurrences_revealed: int,
                game_type: str) -> str:
    """Return the player to play in the next turn in a game of type 
    game_type, given the number of occurrences_revealed. 
    
    Note that in a HUMAN game, the player never changes, regardless of
    the value of occurrences_revealed.
       
    >>> next_player('Player Two', 1, 'PVE')
    'Player Two'
    >>> next_player('Player One', 0, 'PVP')
    'Player Two'
    >>> next_player('Player One', 0, 'P1')
    'Player One'
    """
    if (game_type == HUMAN_HUMAN or game_type == HUMAN_COMPUTER and 
        occurrences_revealed == 0):
        if current_player == PLAYER_ONE:
            return PLAYER_TWO
        else:
            return PLAYER_ONE
    else:
        return current_player

def is_fully_hidden(current_view: str, character_index: int, 
                    mystery_message: str) -> bool:
    """Return True if and only if the character at character_index in 
    mystery_message is not revealed anywhere in current_view.
    
    Precondition: 0 <= character_index <= (len(mystery_message) - 1)
    
    >>> is_fully_hidden('ap^le', 1, 'apple')
    False
    >>> is_fully_hidden('ba^a^a', 2, 'banana')
    True
    >>> is_fully_hidden('ea^l g^ey', 6, 'earl grey')
    """
    
    return mystery_message[character_index] not in current_view

def computer_chooses_solve(current_view: str, game_difficulty: str, 
                           remaining_consonants: str) -> bool:
    """Return True if and only if the conditions under which the computer 
    chooses to solve are met in a game of difficulty game_difficulty.
    
    In an EASY game, the computer chooses to solve if remaining_consonants
    is empty. 
    
    In a HARD game, the computer chooses to solve if
    consonants_unguessed is empty, or if at least half the letters 
    in current_view are revealed.
    
    >>> computer_chooses_solve('^^^l g^ey', 'H', 'rslhdcmpfbwvkqxjz')
    True
    >>> computer_chooses_solve('^ppl^', 'E', 'qrstvwxyz')
    False
    >>> computer_chooses_solve('b^n^n^, 'E', '')
    True
    """
    
    return remaining_consonants == '' or (game_difficulty == 'H'
                                          and half_revealed(current_view))

def remove_at_index(remaining_letters: str, character_index: int) -> str:
    """Return remaining_letters with the character at character_index 
    removed, so that the player cannot guess it again. 
    
    If character_index exceeds the valid indices of remaining_letters, 
    remaining_letters is returned unchanged.
        
    >>> remove_at_index('aeiou', 10)
    'aeiou'
     >>> remove_at_index('xyz', -2)
    'xz'
    >>> remove_at_index('bcdfghjklmnpqrstvwxyz', 0)
    cdfghjklmnpqrstvwxyz
    """
    
    if 0 > character_index or len(remaining_letters) <= character_index:
        return remaining_letters
    else:
        return (remaining_letters[:character_index] + 
                remaining_letters[character_index + 1:])