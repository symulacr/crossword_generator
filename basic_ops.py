import random
import time


def generate_random_possibility(words, dim):
    """Génère une possibilité aléatoire pour le placement d'un mot dans la grille.

    Args:
        words (list): Liste des mots disponibles.
        dim (list): Dimensions de la grille.

    Returns:
        dict: Dictionnaire contenant le mot, sa position et sa direction.
    """
    return {
        "word": random.choice(words),
        "location": [random.randint(0, dim[0] - 1), random.randint(0, dim[1] - 1)],
        "D": "S" if random.random() > 0.5 else "E"
    }


def is_within_bounds(word_len, line, column, direction, grid_width, grid_height):
    """Vérifie si le mot peut être placé dans les limites de la grille.

    Args:
        word_len (int): Longueur du mot.
        line (int): Ligne de départ.
        column (int): Colonne de départ.
        direction (str): Direction ('E' pour Est, 'S' pour Sud).
        grid_width (int): Largeur de la grille.
        grid_height (int): Hauteur de la grille.

    Returns:
        bool: True si le mot est dans les limites, False sinon.
    """
    return (direction == "E" and column + word_len <= grid_width) or \
           (direction == "S" and line + word_len <= grid_height)


def collides_with_existing_words(word, line, column, direction, grid):
    """Vérifie si le mot entre en collision avec des mots existants dans la grille.

    Args:
        word (str): Le mot à placer.
        line (int): Ligne de départ.
        column (int): Colonne de départ.
        direction (str): Direction ('E' ou 'S').
        grid (list): Grille actuelle.

    Returns:
        bool: True si collision, False sinon.
    """
    for k, letter in enumerate(word):
        if direction == "E":
            if grid[line][column + k] != 0 and grid[line][column + k] != letter:
                return True
        elif direction == "S":
            if grid[line + k][column] != 0 and grid[line + k][column] != letter:
                return True
    return False


def ends_are_isolated(word, line, column, direction, grid):
    """Vérifie si les extrémités du mot sont isolées.

    Args:
        word (str): Le mot à vérifier.
        line (int): Ligne de départ.
        column (int): Colonne de départ.
        direction (str): Direction ('E' ou 'S').
        grid (list): Grille actuelle.

    Returns:
        bool: True si les extrémités sont isolées, False sinon.
    """
    if direction == "E":
        return is_cell_free(line, column - 1, grid) and is_cell_free(line, column + len(word), grid)
    elif direction == "S":
        return is_cell_free(line - 1, column, grid) and is_cell_free(line + len(word), column, grid)
    return False


def find_new_words(word, line, column, direction, grid, words):
    """Trouve de nouveaux mots créés par l'ajout d'un mot à la grille.

    Args:
        word (str): Le mot à ajouter.
        line (int): Ligne de départ.
        column (int): Colonne de départ.
        direction (str): Direction ('E' ou 'S').
        grid (list): Grille actuelle.
        words (list): Liste des mots valides.

    Returns:
        list: Liste des nouveaux mots trouvés ou None si invalide.
    """
    new_words = []

    for k, letter in enumerate(word):
        if direction == "E":
            if grid[line][column + k] == 0 and \
               (line > 0 and grid[line - 1][column + k] != 0 or line < len(grid) - 1 and grid[line + 1][column + k] != 0):
                poss_word = extract_word(line, column + k, grid, direction)
                if poss_word not in words:
                    return None
                new_words.append({"D": "S", "word": poss_word, "location": [line, column + k]})

        elif direction == "S":
            if grid[line + k][column] == 0 and \
               (column > 0 and grid[line + k][column - 1] != 0 or column < len(grid[0]) - 1 and grid[line + k][column + 1] != 0):
                poss_word = extract_word(line + k, column, grid, direction)
                if poss_word not in words:
                    return None
                new_words.append({"D": "E", "word": poss_word, "location": [line + k, column]})

    return new_words


def extract_word(line, column, grid, direction):
    """Extrait un mot à partir de la grille, en fonction de la direction.

    Args:
        line (int): Ligne de départ.
        column (int): Colonne de départ.
        grid (list): Grille actuelle.
        direction (str): Direction ('E' ou 'S').

    Returns:
        str: Le mot extrait.
    """
    poss_word = []
    if direction == "E":
        while column < len(grid[0]) and grid[line][column] != 0:
            poss_word.append(grid[line][column])
            column += 1
    elif direction == "S":
        while line < len(grid) and grid[line][column] != 0:
            poss_word.append(grid[line][column])
            line += 1
    return ''.join(poss_word)


def is_valid(possibility, grid, words):
    """Détermine si une possibilité est valide dans la grille donnée.

    Args:
        possibility (dict): Dictionnaire contenant le mot, sa position et sa direction.
        grid (list): Grille actuelle.
        words (list): Liste des mots valides.

    Returns:
        bool: True si valide, False sinon.
    """
    i, j = possibility["location"]
    word = possibility["word"]
    D = possibility["D"]

    if not is_within_bounds(len(word), i, j, D, len(grid[0]), len(grid)):
        return False
    if collides_with_existing_words(word, i, j, D, grid):
        return False
    if not ends_are_isolated(word, i, j, D, grid):
        return False

    return True


def score_candidate(candidate_word, new_words):
    """Calcule le score d'un mot candidat.

    Args:
        candidate_word (str): Le mot candidat.
        new_words (list): Liste des nouveaux mots créés.

    Returns:
        int: Score calculé.
    """
    return len(candidate_word) + 10 * len(new_words)


def add_word_to_grid(possibility, grid):
    """Ajoute un mot à la grille.

    Args:
        possibility (dict): Dictionnaire contenant le mot, sa position et sa direction.
        grid (list): Grille actuelle.
    """
    i, j = possibility["location"]
    word = possibility["word"]

    if possibility["D"] == "E":
        grid[i][j:j + len(word)] = list(word)
    elif possibility["D"] == "S":
        for index, letter in enumerate(word):
            grid[i + index][j] = letter


def select_candidate(candidates, scores):
    """Sélectionne le candidat avec le score maximum.

    Args:
        candidates (list): Liste des candidats.
        scores (list): Liste des scores correspondants.

    Returns:
        tuple: Le candidat sélectionné et son score.
    """
    max_score = max(scores)
    idx = scores.index(max_score)
    return candidates[idx], scores[idx]


def compute_occupancy(grid):
    """Calcule le taux d'occupation de la grille.

    Args:
        grid (list): Grille actuelle.

    Returns:
        float: Taux d'occupation.
    """
    return 1 - (sum(x.count(0) for x in grid) / (len(grid) * len(grid[0])))


def create_empty_grid(dimensions):
    """Crée une grille vide avec les dimensions données.

    Args:
        dimensions (list): Dimensions de la grille.

    Returns:
        list: Grille vide.
    """
    return [[0] * dimensions[1] for _ in range(dimensions[0])]


def generate_valid_candidates(grid, words, dim, timeout):
    """Génère de nouveaux candidats valides pour la grille.

    Args:
        grid (list): Grille actuelle.
        words (list): Liste des mots valides.
        dim (list): Dimensions de la grille.
        timeout (int): Temps maximum pour la génération.

    Returns:
        tuple: Liste des candidats, liste des scores et des nouveaux mots.
    """
    candidates = []
    scores = []
    new_words = []
    tries = 0

    start_time = time.time()

    while not candidates and time.time() < start_time + timeout:
        tries += 1
        new = generate_random_possibility(words, dim)

        if not is_valid(new, grid, words):
            continue

        new_words = find_new_words(new["word"], new["location"][0], new["location"][1], new["D"], grid, words)

        if new_words is None:
            new_words = []
            continue

        score = score_candidate(new["word"], new_words)
        candidates.append(new)
        scores.append(score)

    return candidates, scores, new_words


def is_cell_free(line, col, grid):
    """Vérifie si une cellule est libre.

    Args:
        line (int): Ligne de la cellule.
        col (int): Colonne de la cellule.
        grid (list): Grille actuelle.

    Returns:
        bool: True si la cellule est libre, False sinon.
    """
    if line < 0 or col < 0:
        return True
    try:
        return grid[line][col] == 0
    except IndexError:
        return True


def is_isolated(possibility, grid):
    """Détermine si une possibilité est complètement isolée dans la grille.

    Args:
        possibility (dict): Dictionnaire contenant le mot, sa position et sa direction.
        grid (list): Grille actuelle.

    Returns:
        bool: True si isolé, False sinon.
    """
    line, column = possibility["location"]
    word = possibility["word"]
    direction = possibility["D"]

    if not ends_are_isolated(word, line, column, direction, grid):
        return False

    for i in range(len(word)):
        if direction == "E":
            if not is_cell_free(line - 1, column + i, grid) or not is_cell_free(line + 1, column + i, grid):
                return False
        elif direction == "S":
            if not is_cell_free(line + i, column - 1, grid) or not is_cell_free(line + i, column + 1, grid):
                return False

    return True


def basic_grid_fill(grid, occ_goal, timeout, dim, words):
    """Remplit la grille avec des mots valides jusqu'à atteindre l'objectif d'occupation.

    Args:
        grid (list): Grille actuelle.
        occ_goal (float): Objectif d'occupation.
        timeout (int): Temps maximum pour le remplissage.
        dim (list): Dimensions de la grille.
        words (list): Liste des mots valides.

    Returns:
        list: Liste des mots ajoutés.
    """
    start_time = time.time()
    occupancy = 0
    added_words = []

    while occupancy < occ_goal and time.time() - start_time < timeout:
        candidates, scores, new_words = generate_valid_candidates(grid, words, dim, timeout / 10)

        if not candidates:
            continue

        new, new_score = select_candidate(candidates, scores)

        add_word_to_grid(new, grid)
        added_words.append(new)

        for word in new_words:
            added_words.append(word)

        words.remove(new["word"])
        for word in new_words:
            words.remove(word["word"])

        occupancy = compute_occupancy(grid)
        print(f'Word "{new["word"]}" added. Occupancy: {occupancy:.3f}. Score: {new_score}.')
        if new_words:
            print(f'This also created the words: {new_words}')

    return added_words
