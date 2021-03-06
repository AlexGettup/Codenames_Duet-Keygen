import random
import os
from PIL import Image, ImageDraw


# Funcion para crear una matriz de 5x5 y llenarla de W (Neutrales / Whites)
def create_matrix():
    cols = 5
    rows = 5
    arr = [['W' for i in range(cols)] for j in range(rows)]
    return arr


# Funcion auxiliar para representar una matriz
def show_matrix(arr):
    for row in arr:
        print(row)


# Funcion que rellena una matriz dada con un numero 'ran' de asesinos elegidos al azar
def fill_assassins(arr, ran):
    for i in range(ran):
        col = random.randint(0, 4)
        row = random.randint(0, 4)
        while arr[row][col] != 'W':
            col = random.randint(0, 4)
            row = random.randint(0, 4)
        arr[row][col] = 'A'


# Recupera un array de asesinos dada la matriz
def get_assassins(arr):
    result = []
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == 'A':
                result.append((i, j))
    return result


# Funcion que rellena una matriz dada con un numero 'ran' de espias elegidos al azar
def fill_spies(arr, ran):
    for i in range(ran):
        col = random.randint(0, 4)
        row = random.randint(0, 4)
        while arr[row][col] != 'W':
            col = random.randint(0, 4)
            row = random.randint(0, 4)
        arr[row][col] = 'G'


# Recupera un array de espias dada la matriz
def get_spies(arr):
    result = []
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == 'G':
                result.append((i, j))
    return result


# Rellena la matriz con 3 asesinos y 9
def fill_matrix(arr):
    fill_assassins(arr, 3)
    fill_spies(arr, 9)


# Dada una matriz, crea su version en "espejo"
def mirror_matrix(arr):
    b = create_matrix()
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            b[abs(i-4)][abs(j-4)] = arr[i][j]
    return b


# Crea la tarjeta compañera del array dado
def couple(arr):
    mat = create_matrix()
    aux = []
    assassins = get_assassins(arr)
    random.shuffle(assassins)
    # El primer asesino es el mismo en las dos tarjetas, el segundo es un espia, tercero es W
    mat[assassins[0][0]][assassins[0][1]] = 'A'
    mat[assassins[1][0]][assassins[1][1]] = 'G'
    mat[assassins[2][0]][assassins[2][1]] = 'X'
    aux.append((assassins[2][0], assassins[2][1]))

    spies = get_spies(arr)
    random.shuffle(spies)
    for i in range(len(spies)):
        if i < 3:
            mat[spies[i][0]][spies[i][1]] = 'G'
        elif i == 3:
            mat[spies[i][0]][spies[i][1]] = 'A'
        else:
            mat[spies[i][0]][spies[i][1]] = 'X'
            aux.append((spies[i][0], spies[i][1]))
    fill_assassins(mat, 1)
    fill_spies(mat, 5)

    for tup in aux:
        mat[tup[0]][tup[1]] = 'W'
    return mat


# Crea la imagen dada la matriz, distinguiendo entre espias 'G', asesinos 'A' y neutrales 'W'
def create_image(matrix):
    img = Image.new('RGB', (700, 700), color=(152, 106, 70))
    d = ImageDraw.Draw(img)
    d.rectangle([(50, 50), (650, 650)], fill='purple')
    d.rectangle([(100, 100), (600, 600)], fill=(244, 227, 171))
    for i in range(6):
        d.rectangle([(i * 100 + 100, 100), (i * 100 + 100, 600)], fill='black')
        d.rectangle([(100, i * 100 + 100), (600, i * 100 + 100)], fill='black')
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 'G':
                ImageDraw.floodfill(img, (i * 100 + 150, j * 100 + 150), value=(34, 175, 44))
            elif matrix[i][j] == 'A':
                ImageDraw.floodfill(img, (i * 100 + 150, j * 100 + 150), value=(16, 1, 6))
            else:
                ImageDraw.floodfill(img, (i * 100 + 150, j * 100 + 150), value=(239, 224, 167))
    return img


# Devuelve las dos tarjetas dado el modo de juego
def create_game(mode):
    a = create_matrix()
    fill_matrix(a)
    im = create_image(a)

    c = couple(a)
    if mode == 'mirror':
        c = mirror_matrix(c)
    im1 = create_image(c)
    return im, im1


# Crea las carpetas y los archivos para cada para de tarjetas, un numero de veces definido en number_of_prints
def start(number_of_prints):
    for i in range(number_of_prints):
        ima, imb = create_game('mirror')
        if not os.path.exists('./A/'):
            os.makedirs('./A/')
        if not os.path.exists('./B/'):
            os.makedirs('./B/')
        ima.save('./A/' + str(i) + 'A.png')
        imb.save('./B/' + str(i) + 'B.png')
        print('Acabadas keys numero: ' + str(i))


# ---------------------------------------------
# PRUEBAS
# a = create_matrix()
# fill_matrix(a)
# show_matrix(a)
# print()

# b = mirror_matrix(a)
# show_matrix(b)
# print()

# print(get_assassins(a))
# print(get_spies(a))
# c = couple(a)
# show_matrix(c)
# show_matrix(mirror_matrix(c))
# ---------------------------------------------


# START
# De momento, el default a imprimir son 10 por cada cara
num_to_print = 10
start(num_to_print)
