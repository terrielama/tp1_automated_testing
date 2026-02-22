import connect4

from unittest.mock import call, patch

def test_create_game():
    """Testing that we can create a game"""
    # When
    game = connect4.Connect4()


def test_display_board__empty():
    """Testing the display of an empty board"""
    # Given
    game = connect4.Connect4()
    expected_board = """
|      |
|      |
|      |
|      |
|      |
|      |
|      |
͞͞͞͞͞͞͞ 
"""

    # When
    board = game.display_board()

    # Then
    assert board == expected_board


def test_display_board__after_some_plays():
    """Testing the display of after 3 plays
    Player 1 will put a coin in col 2
    Player 2 will put a coin in col 3
    and Player 1 will put a coin in col 2 again
    """
    # Given
    game = connect4.Connect4()
    expected_board = """
|      |
|      |
|      |
|      |
|      |
| O    |
| OX   |
͞͞͞͞͞͞͞ 
"""

    # When
    game.play_column(2)
    game.play_column(3)
    game.play_column(2)
    board = game.display_board()

    # Then
    assert board == expected_board

# ------------------------------

def test_user_scenario():
    game = connect4.Connect4()

    # When
    game.play_column(1)
    game.play_column(2)
    game.play_column(1)
    game.play_column(2)
    game.play_column(1)
    game.play_column(2)
    game.play_column(1)

    # Then
    assert game.has_ended() == True
    assert game.display_result() == game._board + "\nPlayer 1 won"

# ------------------------------
