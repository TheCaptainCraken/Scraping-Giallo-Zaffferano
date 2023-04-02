import os

count = 0
DIR_PATH = 'ricette'
for path in os.scandir(DIR_PATH):
    if path.is_file():
        count += 1

print('Ricette rubate agli amici di Giallo Zafferano:', count)
