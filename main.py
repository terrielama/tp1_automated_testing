"""Loop to play connect4 in terminal"""
import connect4

def main():
    game = connect4.Connect4()
    depth = 3  # suffisant pour un rendu

    while not game.has_ended():
        # Humain (joueur 1)
        col = game.ask_user_his_column()
        game.play_column(col)

        if game.has_ended():
            break

        # IA (joueur 2)
        ai_col = connect4.find_minmax_move(game, depth, 2)
        print(f"L'IA joue colonne {ai_col}")
        game.play_column(ai_col)

    print(game.display_board())
    print("Fin de la partie")



if __name__ == "__main__":
    main()
