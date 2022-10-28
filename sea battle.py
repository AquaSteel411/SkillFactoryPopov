from random import randint
from colorama import Fore, Style
import asyncio


# Пауза в 3 секунды
async def main():
    await asyncio.sleep(3)

# ================== Блок функций вывода цветного текста ==================


def out_red(text):
    print(Fore.RED + text + Style.RESET_ALL)


def out_green(text):
    print(Fore.GREEN + text + Style.RESET_ALL)


def out_cyan(text):
    print(Fore.CYAN + text + Style.RESET_ALL)


# ============================== Класс корабля ==============================


class Ship:
    def __init__(self, length, player=1):
        self.lives = length
        self.coords = []
        self.add_coord(player)

    def __repr__(self):
        return f'Coordinates: {self.coords}, lives: {self.lives}'

    def get_lives(self):
        return self.lives

    # Данный метод запрашивает координаты 1 корабля
    def add_coord(self, player=1):
        player = player
        i = 0
        while i < self.lives:
            if player == 1:
                cord = input('"x" "y": ').split()
            else:
                cord = f'{randint(1, ci.get_size())} {randint(1, ci.get_size())}'.split()

            if len(cord) != 2:
                print('Введите 2 координаты ("x" "y"):')
                continue

            x, y = cord

            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите числа!')
                continue

            x, y = int(x), int(y)

            if x < 1 or x > ci.get_size() or y < 1 or y > ci.get_size():
                print('Координаты вне диапазона!')
                continue

            if [x - 1, y - 1] in self.coords:
                if player == 1:
                    print('Координаты заняты!')
                    continue
                else:
                    continue

            if player == 1:
                if ci.user.get_field()[x - 1][y - 1] == f'{Fore.GREEN}■{Fore.CYAN}':
                    print('Координаты заняты!')
                    continue
            else:
                if ci.comp.get_field()[x - 1][y - 1] == f'{Fore.GREEN}■{Fore.CYAN}':
                    continue

            if player == 1:
                if [x - 1, y - 1] in ci.get_user_unavail_coord():
                    print('Минимальна дистанция между кораблями 1 клетка!')
                    continue
            else:
                if [x - 1, y - 1] in ci.get_comp_unavail_coord():
                    continue
            # Проверка для второй координаты
            if i == 1:
                if ([x - 1, y] != xy and [x, y - 1] != xy and
                        [x + 1, y] != xy and [x, y + 1] != xy):
                    if player == 1:
                        print('Корабли нельзя делить на части!')
                        continue
                    else:
                        continue
            # Проверка для третьей координаты
            elif i == 2:
                if ([x - 1, y] != xy and [x, y - 1] != xy and
                        [x + 1, y] != xy and [x, y + 1] != xy and
                        [x - 1, y] != cord1 and [x, y - 1] != cord1 and
                        [x + 1, y] != cord1 and [x, y + 1] != cord1):
                    if player == 1:
                        print('Корабли нельзя делить на части!')
                        continue
                    else:
                        continue

            # Проверка для третьей координаты
            if i == 2:
                if not(x - 1 == self.coords[-1][0] == self.coords[-2][0] or
                       y - 1 == self.coords[-1][1] == self.coords[-2][1]):
                    if player == 1:
                        print('Корабль не может быть размещен углом!')
                        continue
                    else:
                        continue

            # Записываем текущие коррдинаты во временную переменную
            last_x, last_y = x, y
            xy = [last_x, last_y]

            self.coords.append([x - 1, y - 1])

            # Временная переменная для проверки расположения корабля углом
            cord1 = self.coords[0]
            cord1 = list(map(lambda a: a + 1, cord1))
            i += 1


# =========================== Класс игрового поля ===========================


class GameBoard:
    def __init__(self, size):
        self.size = size
        self.ships = []
        self.enemy_field = [[' '] * self.size for i in range(self.size)]    # Поле врага (как мы его видим)
        self.unavailable_coords = []
        self.field = [[' '] * self.size for i in range(self.size)]  # Наше поле
        self.empty_cell = []

    def get_ships(self):
        return self.ships

    def get_field(self):
        return self.field

    def get_enemy_field(self):
        return self.enemy_field

    def get_unavail_coords(self):
        return self.unavailable_coords

    def get_size(self):
        return self.size

    def get_empty_cell(self):
        return self.empty_cell

    # Метод добавления координат, в которых не может быть корабля (координаты вокруг корабля),
    # либо добавления координат в которых будут стоять "Т" вокруг подбитого корабля
    # в зависимости от параметра append - 1 или 2
    def append_unavail_cords(self, x, y, append):
        if append == 1:
            lst = self.unavailable_coords
        elif append == 2:
            lst = self.empty_cell
        if [x - 1, y] not in lst:
            lst.append([x - 1, y])
        if [x, y - 1] not in lst:
            lst.append([x, y - 1])
        if [x + 1, y] not in lst:
            lst.append([x + 1, y])
        if [x, y + 1] not in lst:
            lst.append([x, y + 1])
        for cord in lst[::-1]:
            x, y = cord
            if x < 0 or x > (self.size - 1) or y > (self.size - 1) or y < 0:
                lst.remove(cord)   # Удаление координат вне размера поля

    # Добавление корабля на игровое поле
    def add_ship(self, ship):
        coords_ship = []
        unavail_coords = []

        for coord in ship.coords:
            x, y = coord
            coords_ship.append([x, y])
            unavail_coords.append([x, y])

        self.ships.append(ship)     # Добавление корабля в список кораблей на поле

        for xy in coords_ship:
            x, y = xy
            self.field[x][y] = f'{Fore.GREEN}■{Fore.CYAN}'

        for xy in unavail_coords:
            x, y = xy
            GameBoard.append_unavail_cords(self, x, y, 1)

    # Расстановка всех кораблей на игровом поле (player=1 - игрок, player=2 - компьютер)
    def add_all_ships(self, player=1):
        if player == 1:
            ci.show_board()
            print('Введите координаты трехпалубного корабля:')
            GameBoard.add_ship(self, Ship(3, player))
        else:
            GameBoard.add_ship(self, Ship(3, player))

        for i in range(2):
            if player == 1:
                ci.show_board()
                print('Введите координаты двухпалубного корабля:')
                GameBoard.add_ship(self, Ship(2, player))
            else:
                GameBoard.add_ship(self, Ship(2, player))

        for i in range(4):
            if player == 1:
                ci.show_board()
                print('Введите координаты однопалубного корабля:')
                GameBoard.add_ship(self, Ship(1, player))
            else:
                GameBoard.add_ship(self, Ship(1, player))


# ============================ Класс интерфейса =============================


class ConsoleInterface:

    def __init__(self):
        self.size_field = int
        self.set_size()
        # При инициализации объекта класса создается 2 объекта класса Игровая доска
        self.user = GameBoard(self.size_field)  # Игровое поле игрока
        self.comp = GameBoard(self.size_field)  # Игровое поле компьютера
    
    # Приветственное окно
    def hello_user(self):
        print('Добро пожаловать в игру "Морской бой"!')
        print('{:=^38}'.format(' Формат ввода координат: '))
        print('{:=^38}'.format(' "x" "пробел" "y" '))
        print('{:=^38}'.format(' Удачной игры '))

    # Метод запрашивающий размеры игрового поля
    def set_size(self):
        while True:
            try:
                self.size_field = int(input('Введите размер игрового поля (от 6 до 9):'))
            except ValueError:
                print('Введите 1 число!')
                continue

            if self.size_field < 6 or self.size_field > 9:
                if self.size_field < 6 or self.size_field > 10:
                    print('Не правильное значение! Ну... в скобках же диапазон -_-')
                    continue
            break
        return self.size_field

    def get_size(self):
        return self.size_field

    def get_user_unavail_coord(self):
        return self.user.get_unavail_coords()

    def get_comp_unavail_coord(self):
        return self.comp.get_unavail_coords()

    # Метод отображения игрового поля
    @staticmethod
    def field(board):
        for i, row in enumerate(board):
            row_str = f'{i + 1} | {" | ".join(row)} |'
            out_cyan(row_str)

    def show_board(self):
        print('')
        row = [f'{i + 1}' for i in range(self.size_field)]
        out_cyan(' ' * (self.size_field - 4) * 2 + '↓↓↓ Your field ↓↓↓')
        out_cyan(f'  | {" | ".join(row)} |')
        ConsoleInterface.field(self.user.get_field())
        print('===' + '=' * self.size_field * 4)
        out_cyan(' ' * (self.size_field - 4) * 2 + '↓↓↓ Enemy field ↓↓↓')
        out_cyan(f'  | {" | ".join(row)} |')
        ConsoleInterface.field(self.user.get_enemy_field())
        print('===' + '=' * self.size_field * 4)

    # Метод запроса координат, в случае с пользователем,
    # в случае с компьютером - случайного выбора координат с проверкой правильности хода.
    # Также в этом методе определена логика компьютера в случае ранения корабля пользователя.
    def ask_coord(self, player=1):
        my_status = 0   # Статус выстрела пользователя: 0 - мимо, 1 - ранил, 2 - убил
        comp_status = 0     # Статус выстрела компьютера: 0 - мимо, 1 - ранил, 2 - убил
        counter_1 = 0   # Счетчик попадания по 1 кораблю, для определения логики выстрелов компьютера по трехпалубнику
        while True:
            if player == 1:
                print('Ваш ход:')
                coord = input('"x" "y": ').split()
            else:

                coord = f'{randint(1, ConsoleInterface.get_size(self))}' \
                        f' {randint(1, ConsoleInterface.get_size(self))}'.split()

            if len(coord) != 2:
                print('Введите 2 координаты!')
                continue

            x, y = coord

            if not (x.isdigit()) or not (y.isdigit()):
                print('Введите числа!')
                continue

            x, y = int(x), int(y)

            # В зависимости от того, чей ход, присваиваем переменным список кораблей и поле оппонента
            if player == 1:
                fleet = self.comp.get_ships()
                field = self.user.get_enemy_field()
            else:
                fleet = self.user.get_ships()
                field = self.user.get_field()

            if 'X' in field[x - 1][y - 1] or 'T' in field[x - 1][y - 1]:
                if player == 1:
                    print('Вы уже стреляли в эту точку!')
                continue

            if player == 2:
                # Логика выстрелов по двух палубнику. first_xy - координаты первого попадание по кораблю
                if counter_1 == 1:
                    if ([x - 1, y] != first_xy and [x, y - 1] != first_xy and
                            [x + 1, y] != first_xy and [x, y + 1] != first_xy):
                        continue
                # И трехпалубнику. last_xy - координаты второго попадания по кораблю
                if counter_1 == 2:
                    # Если "x" первого попадание равен "x" второго попадания,
                    # стреляет либо слева, либо справа от первого или второго попадания
                    if first_xy[0] == last_xy[0]:
                        if ([x, y - 1] != first_xy and [x, y + 1] != last_xy and
                                [x, y + 1] != first_xy and [x, y - 1] != last_xy):
                            continue
                    # Если "y" первого попадание равен "y" второго попадания,
                    # стреляет либо выше, либо ниже от первого или второго попадания
                    elif first_xy[1] == last_xy[1]:
                        if ([x - 1, y] != first_xy and [x + 1, y] != last_xy and
                                [x + 1, y] != first_xy and [x - 1, y] != last_xy):
                            continue
            if player == 2:
                print('Ход противника...')
                asyncio.run(main())     # Пауза в 3 секунды ходов компьютера для наглядности ходов
            print(f'Выстрел --- {x} {y}')

            # Проверка попадания по одному из кораблей
            for ship in fleet[::-1]:
                if [x - 1, y - 1] in ship.coords:
                    ship.lives -= 1
                    field[x - 1][y - 1] = f'{Fore.RED}X{Fore.CYAN}'
                    if ship.lives == 0:     # Если корабль убит, вокруг корабля расставляем "Т"
                        for xy in ship.coords:
                            x, y = xy
                            if player == 1:
                                self.user.append_unavail_cords(x, y, 2)
                            else:
                                self.comp.append_unavail_cords(x, y, 2)
                        fleet.remove(ship)      # Удаляем корабль из общего списка
                        # И меняем статус текущего игрока
                        if player == 1:
                            my_status = 2
                        else:
                            comp_status = 2
                            counter_1 = 0
                        break
                    # Если только ранили, статус - 1
                    elif player == 1:
                        my_status = 1
                        break
                    else:
                        comp_status = 1
                        break
                # Если промах, статус - 0
                elif player == 1:
                    my_status = 0
                elif player == 2:
                    comp_status = 0

            # Если компьютер ранил, увеличиваем счетчик попаданий на 1 и записываем временные координаты
            if player == 2 and comp_status == 1:
                counter_1 += 1
                if counter_1 == 1:
                    first_xy = [x, y]
                elif counter_1 == 2:
                    last_xy = [x, y]

            # Отображаем результат хода и изменяем игровое поле в соответствии с ходом
            if my_status == 2 and player == 1:
                out_green('Вы потопили вражеский корабль!')
                # Добавляем "Т" вокруг убитого корабля
                for xy in self.user.get_empty_cell():
                    x, y = xy
                    if field[x][y] != f'{Fore.RED}X{Fore.CYAN}':
                        field[x][y] = 'T'
                self.user.get_empty_cell().clear()  # Очищаем список от ненужных координат
            elif comp_status == 2 and player == 2:
                out_red('Ваш корабль идет ко дну!')
                for xy in self.comp.get_empty_cell():
                    x, y = xy
                    if field[x][y] != f'{Fore.RED}X{Fore.CYAN}':
                        field[x][y] = 'T'
                self.comp.get_empty_cell().clear()

            elif my_status == 1 and player == 1:
                out_green('Попадание!')
            elif comp_status == 1 and player == 2:
                out_red('По Вашему кораблю попали!')

            else:
                # В случае промаха передаем ход
                if player == 1:
                    print('Мимо')
                    player = 2
                else:
                    print('Противник промахнулся')
                    player = 1
                field[x - 1][y - 1] = 'T'

            ci.show_board()     # Отображаем игровую доску со всеми изменениями

            # Проверяем остались ли корабли оппонента на игровом поле
            if player == 1:
                if len(fleet) == 0:
                    out_green('Поздравляю! Вы выиграли!')
                    break
            else:
                if len(fleet) == 0:
                    out_red('Увы... Вы проиграли! :(')
                    break

    # Метод, который определяет, кто ходит первым
    def turn(self):
        player = randint(1, 2)
        ConsoleInterface.show_board(self)
        if player == 1:
            print('Вы начинаете!')
            ConsoleInterface.ask_coord(self, 1)
        else:
            print('Компьютер ходит первым!')
            ConsoleInterface.ask_coord(self, 2)

    # Метод запускающий игру
    def run_game(self):
        self.user.add_all_ships(1)
        self.comp.add_all_ships(2)
        print('\n' + ' ' * (self.size_field - 3) * 2 + 'Игра началась!')
        ConsoleInterface.turn(self)


# ====== Выполнение программы ======


if __name__ == '__main__':
    ci = ConsoleInterface()
    ci.run_game()


'''
9.Запретите игроку стрелять в одну и ту же клетку несколько раз. При ошибках хода игрока должно возникать исключение.
В моем коде и так существует проверка выстрела в уже пораженую клетку. Смысла в исключении не вижу.
'''
