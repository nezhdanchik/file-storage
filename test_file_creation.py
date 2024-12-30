import os
words = ['блины', 'бананы', 'булки', 'яблоки', 'мандарины', 'морковь',
         'картошка', 'капуста', 'котлеты', 'колбаса', 'конфеты', 'креветки',
         'крабы']

target_size = 15 * 1024 * 1024
filename = 'normal-file.txt'
with open(filename, 'w', encoding='utf-8') as f:
    while os.stat(filename).st_size < target_size:
        f.write(' '.join(words * 10))