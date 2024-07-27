import os
import pprint
import shutil
import subprocess
import tempfile


def read_word_list(filename, min_length=2, min_different_letters=2):
    """Lit un fichier et retourne une liste de mots. Chaque mot doit être sur une ligne.
    
    Args:
        filename (str): Le nom du fichier à lire.
        min_length (int): Longueur minimale des mots à inclure.
        min_different_letters (int): Nombre minimum de lettres différentes dans le mot.

    Returns:
        list: Liste des mots valides.
    """
    words = []

    with open(filename, encoding='latin1') as words_file:
        for line in words_file:
            word = line.strip()
            if len(word) > min_length and len(set(word)) > min_different_letters:
                words.append(word)

    return words


def write_grid_to_file(grid, out_file="table.tex", out_pdf="out.pdf", keep_tex=False, words=[]):
    """Écrit la grille générée dans un fichier LaTeX et compile en PDF.

    Args:
        grid (list): Grille à écrire, sous forme de liste de listes.
        out_file (str): Nom du fichier de sortie LaTeX.
        out_pdf (str): Nom du fichier PDF de sortie.
        keep_tex (bool): Si True, conserve le fichier .tex après compilation.
        words (list): Liste des mots utilisés dans la grille.
    """
    with open(out_file, "w") as texfile:
        # Écrire le préambule
        texfile.write("\documentclass[a4paper]{article}\n")
        texfile.write(r"\usepackage[utf8]{inputenc}\n")
        texfile.write(r"\usepackage[table]{xcolor}\n")
        texfile.write(r"\usepackage{multicol}\n")
        texfile.write(r"\usepackage{fullpage}\n")
        texfile.write(r"\usepackage{graphicx}\n\n")
        texfile.write(r"\begin{document}\n")
        texfile.write(r"\section*{Challenge}\n")

        # Écrire la grille
        write_grid_to_tex(texfile, grid)

        # Écrire les mots utilisés
        if words:
            write_words_section(texfile, words)

        # Écrire la solution
        texfile.write(r"\newpage\n")
        texfile.write(r"\section*{Solution}\n")
        write_grid_to_tex(texfile, grid, is_solution=True)

        # Fin du document
        texfile.write("\end{document}\n")

    compile_latex(out_file, out_pdf, keep_tex)


def write_grid_to_tex(texfile, grid, is_solution=False):
    """Écrit la grille dans le fichier LaTeX.

    Args:
        texfile: Fichier LaTeX à écrire.
        grid (list): Grille à écrire.
        is_solution (bool): Indique si la grille est la solution.
    """
    texfile.write(r"\resizebox{\textwidth}{!}{\n")
    texfile.write(r"\begin{tabular}{|" + "c|" * len(grid[0]) + "}\n\hline\n")

    for line in grid:
        for index, element in enumerate(line):
            if element == 0:
                texfile.write(r"\cellcolor{black}0")
            else:
                texfile.write(str(element))
            if index != len(line) - 1:
                texfile.write(" & ")
        texfile.write(r"\\ \hline\n")

    texfile.write(r"\end{tabular}\n")
    texfile.write(r"}\n")


def write_words_section(texfile, words):
    """Écrit la section des mots utilisés dans le fichier LaTeX.

    Args:
        texfile: Fichier LaTeX à écrire.
        words (list): Liste des mots utilisés.
    """
    texfile.write(r"\section*{Words used for the problem}\n")
    texfile.write(r"\begin{multicols}{4}\n")
    texfile.write(r"\noindent\n")

    words.sort(key=lambda word: (len(word), word[0]))
    for word in words:
        texfile.write(word + r"\\" + "\n")

    texfile.write(r"\end{multicols}\n")


def compile_latex(out_file, out_pdf, keep_tex):
    """Compile le fichier LaTeX en PDF.

    Args:
        out_file (str): Nom du fichier LaTeX à compiler.
        out_pdf (str): Nom du fichier PDF de sortie.
        keep_tex (bool): Si True, conserve le fichier .tex après compilation.
    """
    print("\n=== Compiling the generated LaTeX file! ===")
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        shutil.copy(out_file, tmpdir)
        os.chdir(tmpdir)
        os.rename(out_file, "out.tex")

        proc = subprocess.call(['pdflatex', "out.tex"])

        shutil.copy("out.pdf", os.path.join(original_dir, out_pdf))
        os.chdir(original_dir)

    print("=== Done! ===\n")

    if not keep_tex:
        os.remove(out_file)


def write_grid_to_screen(grid, words_in_grid):
    """Affiche la grille et les mots utilisés à l'écran.

    Args:
        grid (list): Grille à afficher.
        words_in_grid (list): Liste des mots utilisés dans la grille.
    """
    print("Final grid:")
    for line in grid:
        print(" ".join(str(element) for element in line))

    print("Words:")
    pprint.pprint(words_in_grid)
