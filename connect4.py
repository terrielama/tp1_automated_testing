class Connect4:

    # Plateau initial vide
    _board = """
|      |
|      |
|      |
|      |
|      |
|      |
|      |
͞͞͞͞͞͞͞ 
"""


    # ------------------------------
    def ask_user_his_column(self):
        """Récupère le coup de l'utilisateur via le terminal"""
        print(self.display_board())
        col = int(input("Dans quelle colonne 1 (gauche) à 6 (droite) mettez-vous une pièce ?"))

        # Vérification des bornes
        if col < 1 or col > 6 or not isinstance(col, int):
            col = int(input("Tu ne peux pas jouer colonne " + str(col) + ". Veuillez donner une valeur en [1-6]"))     

        # Vérifie si la colonne est pleine
        elif self.column_full(col):
            col = int(input("Colonne " + str(col) + " est plein. Veuillez en choisir un autre dans " + str(self.list_legal_moves())))  

        return col


    # ------------------------------
    def display_board(self):
        """Affiche le plateau actuel"""
        return self._board


    # ------------------------------
    def play_column(self, move):
        """Simule un coup dans la colonne choisie"""
        col = move
        lines = self._board.split('\n')
        total = self._board.count('O') + self._board.count('X')

        # Descend la colonne pour placer le pion
        for i in range(len(lines)-2, 0, -1):
            if lines[i][col] == ' ':
                if total % 2 == 0:
                    lines[i] = lines[i][:col] + 'O' + lines[i][col+1:]
                else:
                    lines[i] = lines[i][:col] + 'X' + lines[i][col+1:]
                break

        self._board = '\n'.join(lines)


    # ------------------------------
    def column_full(self, col):
        """Vérifie si une colonne est pleine"""
        lines = self._board.split('\n')
        return lines[1][col] != ' '


    # ------------------------------
    def list_legal_moves(self) -> list[int]:
        """Retourne les colonnes jouables"""
        return [i for i in range(1,7) if not self.column_full(i)]


    # ------------------------------
    def has_ended(self):
        """Indique si la partie est terminée"""
        return self.has_winner(self._board)


    # ------------------------------
    def display_result(self):
        """Affiche le résultat de la partie"""
        if self.has_ended():
            return self._board + "\nPlayer 1 won"


    # ------------------------------
    def has_winner(self, board):
        """Vérifie s'il y a un gagnant"""
        lines = board.split('\n')
        if (self.horizontal_victory(lines) or self.vertical_victory(lines)
            or self.diagonal_right_victory(lines) or self.diagonal_left_victory(lines)):
            return True
        else:
            return False


    # ------------------------------
    def eval_position(self, player_id):
        """Évalue la position pour un joueur"""
        my_score = self._count_potential_alignments(player_id)
        other_id = 2 if player_id == 1 else 1
        other_score = self._count_potential_alignments(other_id)
        return my_score - other_score


    # ------------------------------
    def _count_potential_alignments(self, player_id):
        """Compte les alignements potentiels du joueur"""
        symbol = 'O' if player_id == 1 else 'X'
        opponent_symbol = 'X' if player_id == 1 else 'O'
        total_potential = 0
        lines = self._board.strip().split('\n')
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for row in range(7):
            for col in range(1, 7):
                if lines[row][col] == symbol:
                    for dr, dc in directions:
                        for shift in range(4):
                            start_r = row - shift * dr
                            start_c = col - shift * dc
                            if self._is_valid_potential_window(lines, start_r, start_c, dr, dc, opponent_symbol):
                                total_potential += 1
        return total_potential


    # ------------------------------
    def _is_valid_potential_window(self, lines, row, col, dr, dc, opponent_symbol):
        """Vérifie si une fenêtre de 4 cases est possible"""
        for i in range(4):
            nr, nc = row + i * dr, col + i * dc
            if not (0 <= nr < 7 and 1 <= nc <= 6):
                return False
            if lines[nr][nc] == opponent_symbol:
                return False
        return True


    # ------------------------------
    def horizontal_victory(self, lines):
        """Vérifie victoire horizontale"""
        for row in range(len(lines)-2, 0, -1):
            for col in range(1, 4):
                line_str = ''
                for i in range(4):
                    if col + i < 7:
                        line_str += lines[row][col + i]
                if 'OOOO' in line_str or 'XXXX' in line_str:
                    return True
        return False


    # ------------------------------
    def vertical_victory(self, lines):
        """Vérifie victoire verticale"""
        for col in range(1, 7):
            for row in range(len(lines)-2, 2, -1):
                column_str = ''
                for i in range(4):
                    if row - i >= 0 and row - i < len(lines) and col < len(lines[row - i]):
                        column_str += lines[row - i][col]
                if 'OOOO' in column_str or 'XXXX' in column_str:
                    return True
        return False


    # ------------------------------
    def diagonal_right_victory(self, lines):
        """Vérifie victoire diagonale droite (/)"""
        for row in range(len(lines)-2, 2, -1):
            for col in range(1, 7):
                column_str = ''
                for i in range(4):
                    if 0 <= row + i < len(lines) and 0 <= col - i < len(lines[row + i]):
                        column_str += lines[row + i][col - i]
                if 'OOOO' in column_str or 'XXXX' in column_str:
                    return True
        return False


    # ------------------------------
    def diagonal_left_victory(self, lines):
        """Vérifie victoire diagonale gauche (\)"""
        for row in range(len(lines)-2, 2, -1):
            for col in range(1, 7):
                column_str = ''
                for i in range(4):
                    if 0 <= row + i < len(lines) and 0 <= col + i < len(lines[row + i]):
                        column_str += lines[row + i][col + i]
                if 'OOOO' in column_str or 'XXXX' in column_str:
                    return True
        return False


    # ------------------------------
    def _sum_coin_value(self, player_id):
        """Somme les valeurs de toutes les pièces du joueur"""
        symbol = 'O' if player_id == 1 else 'X'
        total_score = 0
        lines = self._board.split('\n')

        for row in range(6):
            board_row = 7 - row         
            row_str = lines[board_row]
            for col in range(7):
                if row_str[col + 1] == symbol:
                    total_score += self.COIN_VALUES[row][col]
        return total_score


    # ------------------------------
    def copy(self):
        """Crée une copie indépendante du jeu"""
        game = self.__class__()
        game._board = self._board
        return game


# ------------------------------
# Algorithme Minimax pour optimiser les coups
def minimax(game, depth, player_id):
    score = game.eval_position(player_id)

    if depth == 0 or game.has_ended():
        return score

    moves = game.list_legal_moves()
    if not moves:
        return game.eval_position(player_id)

    # MAX
    if (game._board.count('O') + game._board.count('X')) % 2 == (player_id - 1):
        best_val = float('-inf')
        for move in moves:
            clone = game.copy()
            clone.play_column(move)
            best_val = max(best_val, minimax(clone, depth - 1, player_id))
        return best_val

    # MIN
    else:
        best_val = float('inf')
        for move in moves:
            clone = game.copy()
            clone.play_column(move)
            best_val = min(best_val, minimax(clone, depth - 1, player_id))
        return best_val


# ------------------------------
def find_minmax_move(game, depth, player_id):
    """Retourne le meilleur coup pour un joueur avec Minimax"""
    best_move = None
    best_score = float('-inf')

    for move in game.list_legal_moves():
        clone = game.copy()
        clone.play_column(move)
        score = minimax(clone, depth - 1, player_id)
        if score >= best_score:
            best_score = score
            best_move = move
    return best_move