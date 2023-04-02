import os
import json
from shutil import move

categorie = []  # Here all the categories will be saved.

# Check every recipe in the 'ricette' folder for its category then if it's not already in the list: save it.
for path in os.scandir('ricette'):
    if path.is_file():
        with open(path.path, 'r') as file:
            try:
                data = json.load(file)
            except:
                print(path.path)
                continue
            if data['categoria'] not in categorie:
                categorie.append(data['categoria'])

# Create a subfolder for every category.
for categoria in categorie:
    if not os.path.exists(f'ricette/{categoria}'):
        os.mkdir(f'ricette/{categoria}')

# Move every recipe in the right subfolder. If a recipe does not have a category the it will not be moved.
for ricetta in os.scandir('ricette'):
    if ricetta.is_file():
        with open(ricetta.path) as file_ricetta:
            data_ricetta = json.load(file_ricetta)
        categoria_ricetta = data_ricetta['categoria']
        try:
            move(ricetta.path, f'ricette/{categoria_ricetta}')
        except:
            print(
                f'Could not move {ricetta.path} in ricette/{categoria_ricetta}')
            continue
