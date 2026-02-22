class Nim:
    def __init__(self, nb_sticks: int):
        # Initialise le jeu avec un nombre de bâtons
        self._sticks_left = nb_sticks
        self._player = 1


    # ------------------------------
    def play_move(self, nb_sticks: int):
        # Retire le nombre de bâtons choisi
        self._sticks_left -= nb_sticks

        # Change de joueur après le coup
        self._player = 2 if self._player == 1 else 1


    # ------------------------------
    def list_legal_moves(self) -> list[int]:
        # Le joueur peut retirer jusqu'à 3 bâtons
        # Il ne peut pas retirer le dernier bâton

        max_sticks = min(3, self._sticks_left - 1)

        # Retourne les coups possibles
        return range(1, max_sticks + 1)


    # ------------------------------
    def eval_position(self, player_id: int):
        # Si il reste un seul bâton, la partie est finie
        if self._sticks_left == 1:

            # Si c'est au joueur courant de jouer, il perd
            if player_id == self._player:
                return -1
            else:
                return 1

        # Sinon la position n'est pas terminale
        else:
            return 0


    # ------------------------------
    def copy(self):
        # Crée une copie indépendante du jeu
        game = self.__class__(self._sticks_left)
        game._player = self._player
        return game


# ------------------------------
# Algorithme optimisant les coups - algorithme Min-Max

# ------------------------------
def minimax(game, depth, player_id):
    # Évalue la position actuelle
    score = game.eval_position(player_id)

    # Condition d'arrêt : position finale ou profondeur atteinte
    if score != 0 or depth == 0:
        return score

    # Liste des coups possibles
    moves = game.list_legal_moves()

    # Si aucun coup possible
    if not moves:
        return game.eval_position(player_id)

    # Si c'est au joueur principal de jouer → on maximise
    if game._player == player_id:
        best_val = float('-inf')

        for move in moves:
            clone = game.copy()
            clone.play_move(move)

            # On garde la meilleure valeur
            best_val = max(best_val, minimax(clone, depth - 1, player_id))

        return best_val

    # Sinon c'est l'adversaire → on minimise
    else:
        best_val = float('inf')

        for move in moves:
            clone = game.copy()
            clone.play_move(move)

            # L'adversaire cherche à réduire notre score
            best_val = min(best_val, minimax(clone, depth - 1, player_id))

        return best_val


# ------------------------------
def find_minmax_move(game, depth):
    # Initialise le meilleur coup et le meilleur score
    best_move = None
    best_score = float('-inf')

    # On mémorise le joueur actuel
    current_player = game._player

    # On teste tous les coups possibles (ordre décroissant)
    for move in sorted(game.list_legal_moves(), reverse=True):
        clone = game.copy()
        clone.play_move(move)

        # Évalue le coup avec minimax
        score = minimax(clone, depth - 1, current_player)

        # On garde le coup ayant le meilleur score
        if score >= best_score:
            best_score = score
            best_move = move

    return best_move