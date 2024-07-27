#!/usr/bin/python3
""" Crossword Generator

Ce script prend une liste de mots et crée une nouvelle table LaTeX représentant un
puzzle de mots croisés, qui est ensuite imprimée au format PDF. Vous pouvez ensuite
l'imprimer sur du papier, si cela vous intéresse.
"""

# Imports standards
import argparse

# Imports personnalisés
import file_ops
import grid_generator
from grid_generator import GridGenerator


def parse_cmdline_args():
    """Utilise argparse pour obtenir les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(description='Generate a crossword puzzle.')
    parser.add_argument('-f', type=str, default="words.txt", dest="word_file",
                        help="Un fichier contenant des mots, un mot par ligne.")
    parser.add_argument('-d', type=int, nargs="+", default=[20, 20], dest="dim",
                        help="Dimensions de la grille à construire.")
    parser.add_argument('-n', type=int, default=1, dest="n_loops",
                        help="Nombre de boucles d'exécution à effectuer.")
    parser.add_argument('-t', type=int, default=10, dest="timeout",
                        help="Temps d'exécution maximum, en secondes, par boucle d'exécution.")
    parser.add_argument('-o', type=float, default=1.0, dest="target_occ",
                        help="Occupation désirée de la grille finale. Par défaut, 1.0, ce qui utilise tout le temps alloué.")
    parser.add_argument('-p', type=str, default="out.pdf", dest="out_pdf",
                        help="Nom du fichier PDF de sortie.")
    parser.add_argument('-a', type=str, default="basic", dest="algorithm",
                        help="L'algorithme à utiliser.")

    return parser.parse_args()


def create_generator(algorithm, word_list, dimensions, n_loops, timeout, target_occupancy):
    """Construit l'objet générateur pour l'algorithme donné."""
    algorithm_class_map = {"basic": GridGenerator}

    if algorithm not in algorithm_class_map:
        print(f"Could not create generator object for unknown algorithm: {algorithm}.")
        return None

    return algorithm_class_map[algorithm](word_list, dimensions, n_loops, timeout, target_occupancy)


def main():
    # Analyse des arguments
    args = parse_cmdline_args()

    # Lecture des mots depuis le fichier
    words = file_ops.read_word_list(args.word_file)
    print(f"Read {len(words)} words from file.")

    # Construction de l'objet générateur
    dim = args.dim if len(args.dim) == 2 else [args.dim[0], args.dim[0]]
    generator = create_generator(args.algorithm, words, dim, args.n_loops, args.timeout, args.target_occ)
    if not generator:
        return

    # Génération de la grille
    generator.generate_grid()

    # Écriture de la grille
    grid = generator.get_grid()
    words_in_grid = generator.get_words_in_grid()
    file_ops.write_grid_to_file(grid, words=[word for word in words_in_grid], out_pdf=args.out_pdf)
    file_ops.write_grid_to_screen(grid, words_in_grid)


if __name__ == "__main__":
    main()
