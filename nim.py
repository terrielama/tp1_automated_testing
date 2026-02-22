class Nim:
    def __init__(self, nb_sticks: int):
        self._sticks_left = nb_sticks
        self._player = 1

    def play_move(self, nb_sticks: int):
        self._sticks_left -= nb_sticks
        self._player = 2 if self._player == 1 else 1

    def list_legal_moves(self) -> list[int]:
        # Player can remove up to 3 sticks
	    # Player is not allowed to remove last stick
        max_sticks = min(3, self._sticks_left - 1)
        return range(1, max_sticks + 1)

    def eval_position(self, player_id: int):
        if self._sticks_left == 1:
            if player_id == self._player:
                return -1
            else :
                return 1
                
        else:
            return 0

    def copy(self):
        game = self.__class__(self._sticks_left)
        game._player = self._player
        return game
    

def minimax(game, depth, player_id):
    score = game.eval_position(player_id)
    if score != 0 or depth == 0:
        return score

    moves = game.list_legal_moves()
    if not moves:
        return game.eval_position(player_id)

    if game._player == player_id:
        best_val = float('-inf')
        for move in moves:
            clone = game.copy()
            clone.play_move(move)
            best_val = max(best_val, minimax(clone, depth - 1, player_id))
        return best_val
    else:
        best_val = float('inf')
        for move in moves:
            clone = game.copy()
            clone.play_move(move)
            best_val = min(best_val, minimax(clone, depth - 1, player_id))
        return best_val

def find_minmax_move(game, depth):
    best_move = None
    best_score = float('-inf')
    current_player = game._player

    for move in sorted(game.list_legal_moves(), reverse=True): 
        clone = game.copy()
        clone.play_move(move)
        score = minimax(clone, depth - 1, current_player)
        
        if score >= best_score:
            best_score = score
            best_move = move
            
    return best_move