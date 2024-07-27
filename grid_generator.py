import basic_ops


class GridGenerator:
    def __init__(self, word_list, dimensions, n_loops, timeout, target_occupancy):
        self.word_list = word_list
        self.dimensions = dimensions
        self.n_loops = n_loops
        self.timeout = timeout
        self.target_occupancy = target_occupancy
        self.reset()

    def get_grid(self):
        """Retourne la grille actuelle."""
        return self.grid

    def get_words_in_grid(self):
        """Retourne la liste des mots présents dans la grille."""
        return self.words_in_grid

    def generate_grid(self):
        """Met à jour la grille interne avec du contenu."""
        self.reset()
        print(f"Generating {self.dimensions} grid with {len(self.word_list)} words.")

        # Remplissage de la grille avec le nombre recommandé de boucles
        for i in range(self.n_loops):
            print(f"Starting execution loop {i + 1}:")
            self.generate_content_for_grid()

            print("Culling isolated words.")
            self.cull_isolated_words()
            self.reset_grid_to_existing_words()

        occupancy = basic_ops.compute_occupancy(self.grid)
        print(f"Built a grid of occupancy {occupancy:.2f}.")

    def reset(self):
        """Réinitialise la grille et la liste des mots."""
        self.grid = basic_ops.create_empty_grid(self.dimensions)
        self.words_in_grid = []

    def generate_content_for_grid(self):
        """Utilise l'algorithme de remplissage de base pour remplir la grille."""
        new_words = basic_ops.basic_grid_fill(self.grid, self.target_occupancy, self.timeout, self.dimensions, self.word_list)
        self.words_in_grid.extend(new_words)

    def cull_isolated_words(self):
        """Supprime les mots qui sont trop isolés de la grille."""
        isolated_words = [word for word in self.words_in_grid if basic_ops.is_isolated(word, self.grid)]
        
        for word in isolated_words:
            print(f"Culling word: {word}.")
            self.words_in_grid.remove(word)

    def reset_grid_to_existing_words(self):
        """Réinitialise la grille avec les mots présents dans self.words_in_grid."""
        self.grid = basic_ops.create_empty_grid(self.dimensions)

        for word in self.words_in_grid:
            basic_ops.add_word_to_grid(word, self.grid)
