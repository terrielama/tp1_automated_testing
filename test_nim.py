import nim

def test_minmax__nim_4_sticks():
    # Given
    game = nim.Nim(nb_sticks=4)
    move_to_find = 3

    # When
    move = nim.find_minmax_move(game, depth=4)

    # Then
    assert move == move_to_find