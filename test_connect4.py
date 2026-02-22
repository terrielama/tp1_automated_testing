import connect4
from unittest.mock import call, patch


# ------------------------------
def test_create_game():
    """Test de création d'une partie"""
    # Quand on crée un jeu
    game = connect4.Connect4()


# ------------------------------
def test_display_board__empty():
    """Test de l'affichage d'un plateau vide"""
    # Données initiales
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

    # Action
    board = game.display_board()

    # Vérification
    assert board == expected_board


# ------------------------------
def test_display_board__after_some_plays():
    """Test de l'affichage après 3 coups
    Joueur 1 : colonne 2
    Joueur 2 : colonne 3
    Joueur 1 : colonne 2
    """
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

    # Quand on joue les coups
    game.play_column(2)
    game.play_column(3)
    game.play_column(2)

    board = game.display_board()

    # Alors le plateau correspond
    assert board == expected_board


# ------------------------------
def test_user_scenario():
    """Test scénario complet simulé"""
    game = connect4.Connect4()

    # Jouer une séquence de coups
    game.play_column(1)
    game.play_column(2)
    game.play_column(1)
    game.play_column(2)
    game.play_column(1)
    game.play_column(2)
    game.play_column(1)

    # Vérifications
    assert game.has_ended() == True
    assert game.display_result() == game._board + "\nPlayer 1 won"


# ------------------------------
def test_has_winner():
    """Vérifie les situations gagnantes"""
    game = connect4.Connect4()

    # Ligne horizontale
    board = """
|      |
|      |
|      |
|      |
|      |
|      |
|OOOO  |
͞͞͞͞͞͞͞ 
"""
    assert game.has_winner(board) == True

    # Ligne verticale
    board = """
|      |
|      |
|      |
|O     |
|O     |
|O     |
|O     |
͞͞͞͞͞͞͞ 
"""
    assert game.has_winner(board) == True

    # Diagonale (gauche-droite)
    board = """
|      |
|      |
|      |
|     O|
|    O |
|   O  |
|  O   |
͞͞͞͞͞͞͞ 
"""
    assert game.has_winner(board) == True

    # Diagonale (droite-gauche)
    board = """
|      |
|      |
|      |
|O     |
| O    |
|  O   |
|   O  |
͞͞͞͞͞͞͞ 
"""
    assert game.has_winner(board) == True


# ------------------------------
def test_has_illegal_win():
    """Vérifie des positions où une victoire est possible malgré des cases vides"""
    game = connect4.Connect4()

    # Diagonales incomplètes
    board = """
|      |
|      |
|     O|
|    O |
|   O  |
|  O   |
|      |
͞͞͞͞͞͞͞ 
"""
    assert game.has_winner(board) == True

    board = """
|      |
|      |
|O     |
| O    |
|  O   |
|   O  |
|      |
͞͞͞͞͞͞͞ 
"""
    assert game.has_winner(board) == True

    # Colonne incomplète
    board = """
|      |
|      |
|O     |
|O     |
|O     |
|O     |
|      |
͞͞͞͞͞͞͞ 
"""
    assert game.has_winner(board) == True

    # Ligne horizontale incomplète
    board = """
|OOOO  |
|      |
|      |
|      |
|      |
|      |
|      |
͞͞͞͞͞͞͞ 
"""
    assert game.has_winner(board) == True


# ------------------------------
@patch('connect4.input')
def test_ask_user_his_column(mock_input):
    """Test que l'utilisateur est invité jusqu'à fournir un coup valide"""
    mock_input.side_effect = [-1, 2]
    game = connect4.Connect4()

    col = game.ask_user_his_column()

    # Vérifie l'ordre des appels à input
    print(mock_input.call_args_list)
    assert mock_input.call_args_list == [
        call('Dans quelle colonne 1 (gauche) à 6 (droite) mettez-vous une pièce ?'),
        call("Vous ne pouvez pas jouer à la colonne -1. Veuillez donner une valeur dans [1-6]")
    ]
    # Vérifie la colonne renvoyée
    assert col == 2


# ------------------------------
@patch('connect4.input')
def test_ask_user_his_column_not_available(mock_input):
    """Test qu'on ne peut pas jouer dans une colonne pleine"""
    mock_input.side_effect = [2, 3]
    game = connect4.Connect4()
    game._board = """
| O    |
| O    |
| O    |
| O    |
| O    |
| O    |
| O    |
͞͞͞͞͞͞͞ 
"""

    col = game.ask_user_his_column()

    print(mock_input.call_args_list)
    assert col == 3
    assert mock_input.call_args_list == [
        call('Dans quelle colonne 1 (gauche) à 6 (droite) mettez-vous une pièce ?'),
        call("Colonne " + str(2) + " est plein. Veuillez en choisir un autre dans " + str([1,3,4,5,6]))
    ]


# ------------------------------
def test_eval_position_empty_board():
    """Évalue un plateau vide"""
    game = connect4.Connect4()
    assert game.eval_position(1) == 0


# ------------------------------
def test_eval_position_center_vs_corner():
    """Évalue les positions du centre vs coin"""
    game = connect4.Connect4()
    game.play_column(4)  # Joueur 1
    game.play_column(1)  # Joueur 2

    assert game.eval_position(1) == 2
    assert game.eval_position(2) == -2


# ------------------------------
def test_eval_position_blocked_piece():
    """Évalue un pion bloqué horizontalement et verticalement"""
    game = connect4.Connect4()
    game._board = """
    |      |
    |      |
    |      |
    |  X   |  <-- Bloque vertical haut
    | XOX  |  <-- Bloque les côtés
    |  X   |  <-- Bloque vertical bas
    |      |
    ͞͞͞͞͞͞͞ 
    """
    # Le pion O en colonne 3 ne peut plus aligner 4
    score_o = game._count_potential_alignments(1)
    assert score_o == 0


# ------------------------------
def test_eval_position_potential_alignment():
    """Évalue un pion au centre sur plateau vide"""
    game = connect4.Connect4()
    game.play_column(4)  # Joueur 1

    score_initial = game.eval_position(1)
    assert score_initial > 0