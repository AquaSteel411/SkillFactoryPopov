from random import randint


print('\033[36m{:^19}'.format('Start game!'))
print('-------------------')

# Стартовое поле игры
data = {0: '-', 10: '-', 20: '-',
        1: '-', 11: '-', 21: '-',
        2: '-', 12: '-', 22: '-'}
print(f'        0 1 2'
      f'\n      0 {data[0]} {data[10]} {data[20]}'
      f'\n      1 {data[1]} {data[11]} {data[21]}'
      f'\n      2 {data[2]} {data[12]} {data[22]}')
print('\n===================')

# Кидаем жребий, кто будет начинать игру
player = randint(1, 2)
if player == 1:
    print('1st player - you start "X"')
else:
    print('2nd player - you start "O"')

# Возможные ходы, для исключения ввода пользователем несуществующих координат
possible_coordinates = (0, 1, 2, 10, 11, 12, 20, 21, 22)

while True:
    # Проверяем правильность ввода координат и определяем, что ставить в пустую клетку,
    # в зависимости от того, какой игрок ходил: 'X' или 'O'
    while True:
        turn = input('Enter coordinates:')
        print('')
        try:
            turn = int(turn)
        except ValueError:
            # Если пользователь ввел буквенное значение - "Incorrect input, try again :("
            print('Incorrect input, try again! :(')
            continue

        if turn in possible_coordinates and data[turn] == '-':
            data[turn] = 'X' if player == 1 else 'O'
            break
        else:
            print('Incorrect input, try again! :(')

    print(f'        0 1 2'
          f'\n      0 {data[0]} {data[10]} {data[20]}'
          f'\n      1 {data[1]} {data[11]} {data[21]}'
          f'\n      2 {data[2]} {data[12]} {data[22]}')

    # Условие победы
    if (data[0] == data[10] == data[20] == 'X' or data[0] == data[10] == data[20] == 'O' or
            data[1] == data[11] == data[21] == 'X' or data[1] == data[11] == data[21] == 'O' or
            data[2] == data[12] == data[22] == 'X' or data[2] == data[12] == data[22] == 'O' or
            data[0] == data[1] == data[2] == 'X' or data[0] == data[1] == data[2] == 'O' or
            data[10] == data[11] == data[12] == 'X' or data[10] == data[11] == data[12] == 'O' or
            data[20] == data[21] == data[22] == 'X' or data[20] == data[21] == data[22] == 'O' or
            data[0] == data[11] == data[22] == 'X' or data[0] == data[11] == data[22] == 'O' or
            data[20] == data[11] == data[2] == 'X' or data[20] == data[11] == data[2] == 'O'):

        # Если ходил первый игрок - он победитель, иначе выиграл второй игрок
        if player == 1:
            print('\n{:^19}'.format('↓↓↓'))
            print('\033[31m{:^19}' .format('1st player WIN!!!'))

            break
        else:
            print('\n{:^19}'.format('↓↓↓'))
            print('\033[31m{:^19}' .format('2nd player WIN!!!'))
            break

    # Проверяем, остались ли пустые клетки
    if '-' not in data.values():
        print('\n{:^19}'.format('↓↓↓'))
        print('\033[31m{:^19}' .format('DRAW!!!'))
        break

    # Педача хода другому игроку, если ходил первый игрко 'player == 1', передаем ход второму игроку 'player = 2'
    player = 2 if player == 1 else 1
    print('')
    print('===================')
    print('')
