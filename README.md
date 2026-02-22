<!--
$env:Path = "C:\Users\Terrie\.local\bin;$env:Path"
puis
uv run pytest
 -->

# TD1: Tester et coder un Puissance 4

Nous allons coder un Puissance4 (_"Connect4"_ en anglais) en faisant du _"Test-Driven Development"_ (TDD). <br/>
Pour chaque étape, nous allons écrire un test décrivant l'API qu'on voit, puis nous ferons le développement. <br/>
Nous allons d'abord développer un jeu utilisable dans le terminal. <br/>
Puis nous coderons une I.A. basique.

Puissance 4 est un jeu avec une grille de 6 colonnes et 7 rangées. </br>
A tour de rôle, les joueurs mettent une pièce de leur couleur dans une colonne. <br/>
Le 1er joueur à aligner 4 pièces de sa couleur horizontalement, verticalement ou diagonalement gagne. <br/>
Si la grille est remplie et qu'aucune ligne de 4 pièces n'est faite, il y a match nul.

## Installation

### Sur Mac/Linux :

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
uv run pytest
```

### Sur Windows:

#### WSL (recommandé) -> Utilisez l'installation Mac/Linux

#### Windows terminal

```bash
scripts\setup.bat
uv run pytest
```

### PyCharm

Si vous avez PyCharm, cliquez droit sur le dossier "src/" -> "Mark directory as" -> "Sources Root"

## Partie 1: Coder le puissance4

Pour vérifier que tout est bien installé, faites tourner les tests avec la commande:

```bash
uv run pytest
```

Vous devriez voir que 3 tests ont été trouvés, qu'1 est vert et 2 sont rouges.

**ATTENTION:** Si, au bout de 30 minutes, cette commande ne fonctionne pas sur votre ordinateur, vous avez -1 au TD (le TD est sur 5)

### 1.1. Implémenter le cas simple

Etapes:

1. Réussir le test `test_display_board__empty` en implémentant la méthode `display_board` qui va juste retourner la grille vide
2. Réussir le test `test_display_board__after_some_plays` en implémentant la grille de 6 colonnes et 7 rangées dans l'objet `Connect4()` (par exemple, avec un `self._board = np.zeros((7, 6))`. Il faut implémenter la fonction `play_column` et que le `display_board` lise `self._board` pour afficher la grille.
3. Faite un test _"user scenario"_ où une partie va au bout. Le joueur 1 joue toujours dans la 1ère colonne. Le joueur 2 toujours dans la 2nde. Au bout de 4 coups du joueur 1, je veux que `assert game.has_ended() == True` et `assert game.display_result() == "Player 1 won"`.

Pour l'instant, la fonction `has_ended` ne fonctionne **que s'il y a 4 pièces verticales.**
Pour toutes les autres façons de gagner (horizontale, diagonale), nous allons créer les tests pour chaque cas, puis implémenter la logique

### 1.2. Blinder la fonction _"has_ended"_

On va ajouter des tests pour une fonction `has_winner(board) -> bool`. <br/>
On est dans le cas où cette fonction est cruciale, on n'a pas le droit à l'erreur. <br/>
On va d'abord ajouter les cas standards en tests. <br/>
Puis on va imaginer des façons de faire planter la logique, et les ajouter en cas de tests.

Etapes:

1. Ajouter le test pour un gagnant horizontal. Implémenter la logique pour passer le test. Refactorer le code **si vous voyez une refacto évidente**
2. Ajouter un test pour une diagonale "haut droite". Implémenter la logique. Refacto si possible
3. Ajouter un test pour une diagonale "haut gauche". Implémenter la logique. Refacto si possible
4. Essayer d'imaginer des façons de faire planter cette logique. Ajouter les cas de tests

### 1.3 Faire tourner le jeu

Maintenant, en faisant

```bash
uv run python main.py
```

Vous devriez pouvoir jouer à Puissance4

### 1.4 Blinder la partie "ask_user_his_column"

La fonction `ask_user_his_column` récupère le coup jouer par l'utilisateur.<br/>
Beaucoup de problèmes peuvent arriver ici! Le joueur peut inputer une colonne qui n'existe pas (8, -1, "foo"). Pour tester ceci, nous allons utiliser un mock pour simuler les inputs de l'utilisateur.

Voici un exemple de mock pour tester l'utilisation classique:
On fixe que l'utilisateur jouera la column 4.
Quand on appelle ask_user_his_column, on récupère bien qu'il a joué la colonne 4.
On vérifie aussi que le message qu'on lui a envoyé était bien "In which column 1 (left) to 6 (right) do you put a coin".

```python
from unittest.mock import patch

@patch('connect4.input')
def test_ask_user_his_column(mock_input):
    # Given
    col_played = 4
    mock_input.return_value = col_played
    game = connect4.Connect4()

    # When
    col = game.ask_user_his_column()

    # Then
    assert col == col_played
    mock_input.assert_called_once_with("In which column 1 (left) to 6 (right) do you put a coin?")
```

A vous de jouer:

1. Ecrire un test où l'utilisateur met une valeur incorrect (-1, 8, foo). la fonction va raise une value error. Utiliser `with pytest.raises(ValueError): col = game.ask_user_his_column` pour vérifier que, avec un input non valide, on raise une erreur.
2. A posteriori, on se dit qu'on ne veut pas afficher une erreur à notre utilisateur. On veut lui dire "You can't play column {his column}. Please give a value in [...]", puis que l'utilisateur puisse re-inputer un coup. Au lieu d'utiliser `mock_input.return_value` (qui fixe la return value de "input" dans notre test), utiliser `mock__input.side_effect = [-1, 2]`. Dans ce cas, dans ce test, la 1ère fois que le code va appeler "input", il retournera "-1". La 2nde fois, il retournera 2. Utiliser `mock_input.call_args_list` pour voir toutes les fois où `input` a été appelé, avec quels arguments.
3. Faite un plateau où une colonne est remplie (par exemple, la colonne 2). Ecrivez un test pour changer le texte affiché à l'utilisateur (disant qu'il ne peut jouer que colonnes 1 et 3 à 6). Utiliser side-effect pour qu'il joue la colonne interdite (2), puis une colonne acceptable.

## Partie 2: Coder une I.A. (bonus)

### 2.1. Algorithme optimisant les coups

On va faire algorithme Min-Max. <br/>
Avec une fonction `game.eval_position(player_id) -> float` qui indique la valeur d'une position pour le joueur {player_id}, l'algorithme va explorer tous les coups possibles (jusqu'à une profondeur `k`). On suppose à chaque fois que l'adversaire joue le meilleur coup. On choisit le coup qui minimise la valeur du meilleur coup de l'adversaire (on "minimise" le coup "max" de l'adversaire).

Voir (fiche wikipedia)[https://fr.wikipedia.org/wiki/Algorithme_minimax]

Il serait compliqué de tester ça avec le puissance 4. <br/>
Donc on peut choisir un jeu plus simple: un (jeu de nim)[https://fr.wikipedia.org/wiki/Jeux_de_Nim] (ou _"jeu des batonnets"_)<br/>
On suppose qu'on dispose de 10 batons. <br/>
Chaque joueur, a son tour, peut retirer 1, 2 ou 3 batons. <br/>
Le but est de ne pas prendre le dernier baton.

Il existe une technique pour toujours gagner à ce jeu, mais cela n'est pas important ici. <br/>
Ce qui est important est qu'on pourra parcourir tout l'arbre.

Créer un objet Nim qui a les méthodes suivantes:

- init(nb_stick: int) où on choisit le nombre initial de bâtons
- play_move(nb_stick:int) (nb_stick doit être entre 1 et 3)
- list_legal_moves(): liste le nombre de bâtons que peut prendre le joueur.
- eval_position(player_id) qui vaut -1 s'il reste un seul baton et que c'est à {player_id} de jouer, 1 s'il reste un baton et que ce n'est pas à {player_id} de jouer, 0 sinon
- copy(): Créer une copie du jeu

Votre objet Nim ressemblera à ça
src/nim.py

```python
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
        max_sticks = min(3, self._sticks - 1)
        return range(1, max_sticks + 1)

    def eval_position(self, player_id: int):
        if self._sticks_left == 1:
	   if player_id == self._player:
	       return - 1
	   else:
	       return 1
	else:
	   return 0

    def copy(self):
        game = self.__class__(self._sticks_left)
	game._player = self._player
	return game
```

On va implémenter notre algorithme MinMax, mais d'abord on va voir ce qu'il doit nous répondre dans certains cas:

- S'il reste 4 bâtons, l'algorithme doit retourner "retire 3 batons" (et ça gagne)
- S'il reste 6 bâtons, l'algorithme doit retourner "retire 1 batons" (et ça gagne: avec 5 batons, s'il en retire 1, il en reste 4, cas précédent. S'il en retire 2, il en reste 3, on en retire 2 et on gagne...)
- S'il reste 12 bâtons, l'algorithme doit retourner "retire 2 batons" (et ça gagne)

Créer les tests:

```python
def test_minmax__nim_4_sticks():
    # Given
    game = Nim(nb_sticks=4)
    move_to_find = 3

    # When
    move = find_minmax_move(game, depth=4)

    # Then
    assert move == move_to_find
```

Ou, si on veut être fancy:

```python
@pytest.mark.parametrize("nb_sticks,move_to_find, ", [
    (4, 3),
    (6, 1),
    (12, 2),
])
def test_minmax__nim_4_sticks(nb_sticks, move_to_find):
    # Given
    game = Nim(nb_sticks)

    # When
    move = find_minmax_move(game, depth=5)
    # Depth = 5 should be enough for our test cases

    # Then
    assert move == move_to_find
```

Implémenter MinMax algorithm (ou utiliser IA pour générer le code qui marche)

### 2.2. Utiliser MinMax sur le Puissance4

Il faut, pour notre puissance 4, implémenter les fonctions "play_move, list_legal_moves, eval_position".

Nous avions "play_column" qui fait le job de play move. Que fait-on ?

- Nous renommons "play_column" en "play_move" ?
- Nous créons une fonction "def play_move(self, col): return self.play_column(col)" ?
  Pourquoi ?

Pour "eval_position", il faut une heuristique pour savoir si une partie se passe bien ou non. <br/>
On va compter les pièces de chaque joueur, mais toutes les pièces n'ont pas la même valeur: une pièce centrale peut faire beaucoup plus de puissance 4 qu'une pièce dans un coin, donc la pièce centrale vaut plus que la pièce dans un coin.

En comptant le nombre d'alignements qu'une pièce peut faire, nous arrivons sur ce tableau

```python
coin_values = [
    [3, 4, 5, 7, 5, 4, 3],
    [4, 6, 8, 10, 8, 6, 4],
    [5, 8, 11, 13, 11, 8, 5],
    [5, 8, 11, 13, 11, 8, 5],
    [4, 6, 8, 10, 8, 6, 4],
    [3, 4, 5, 7, 5, 4, 3],
]
```

Pour chaque joueur, on somme la valeur des pièces qu'il a.

```python
def eval_position(self, player_id):
    my_coins = self._sum_coin_value(player_id)
    other_player = 2 if player_id == 1 else 1
    other_coints = self._sum_coin_value(other_player)
    return my_coins - other_coins
```

Etapes:

- Créer des tests unitaires pour ce "eval_position" (selon la grille et le joueur, vérifier que le résultat est le bon).
- Changer connect4 ou main.py pour pouvoir jouer contre votre I.A.
- Tester, avec "python main.py"
- La fonction "eval_position" pourrait être améliorée. Si une pièce est bloquée (il y a des pièces adverses qui l'empêche de faire puissance 4), elle ne vaut plus rien. Créer de nouveaux tests où la valeur d'une pièce correspond au nombre d'alignements qu'elle peut faire. Implémenter le code.
#   t p 1 _ a u t o m a t e d _ t e s t i n g  
 