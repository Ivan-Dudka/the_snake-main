from random import choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Координаты всех клеток игрового поля
ALL_POSITIONS = {
    (x * GRID_SIZE, y * GRID_SIZE) for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

# Координаты центра поля:
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    GameObject - это базовый класс, от которого наследуются другие
    игровые объекты.
    """

    def __init__(self) -> None:
        """
        Инициализирует базовые атрибуты объекта,такие как его позиция
        и цвет.
        """
        self.position = SCREEN_CENTER
        self.body_color = None

    def draw(self) -> None:
        """
        Это абстрактный метод, который предназначен для
        переопределения в дочерних классах. Этот метод должен определять,
        как объект будет отрисовываться на экране. По умолчанию — pass.
        """


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject, описывающий яблоко и действия с ним.
    Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def __init__(self):
        """Конструктор класса Apple."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None

    def randomize_position(self, snake_positions):
        """
        Устанавливает случайное положение яблока на игровом поле
        c учётом координат занятых змейкой.
        """
        self.position = choice(tuple(ALL_POSITIONS - set(snake_positions)))

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс унаследованный от GameObject, описывающий змейку
    и действия с ней.
    """

    def __init__(self):
        """Конструктор класса Snake."""
        super().__init__()
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции), добавляя новую
        голову в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.positions.insert(
            0,
            (
                (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
                (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
            )
        )
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние после столкновения
        с собой.
        """
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш, чтобы изменить направление
    движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """Основной цикл игры."""
    # Инициализация pygame:
    pg.init()
    # Создаём экземпляры классов.
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake.positions)
    while True:
        clock.tick(SPEED)
        pg.display.update()
        handle_keys(snake)
        snake.move()
        snake.update_direction()
        snake.draw()
        apple.draw()
        if snake.get_head_position() == apple.position:
            snake.positions.append(snake.last)
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)


if __name__ == '__main__':
    main()
