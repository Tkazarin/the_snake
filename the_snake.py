from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Константный словарь направлений
DIRECTIONS = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс, базовый класс"""

    def __init__(
        self, position_val=None, body_color_val=BOARD_BACKGROUND_COLOR
    ) -> None:
        """Метод инициализации игрового объекта"""
        if position_val is None:
            self.position = SCREEN_CENTER
        else:
            self.position = position_val
        self.body_color = body_color_val

    def draw(self):
        """Заготовка метода для дочерних классов отрисовки объекта"""
        pass


class Apple(GameObject):
    """Класс яблока"""

    def __init__(self, body_color_val=APPLE_COLOR):
        """Метод инициализации объекта класса яблоко"""
        super().__init__(position_val=None, body_color_val=body_color_val)
        self.randomize_position()

    def randomize_position(self):
        """Метод рандомизации положения яблока"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self, body_color_val=SNAKE_COLOR):
        """Метод инициализации объекта класса змейка"""
        super().__init__(position_val=None, body_color_val=body_color_val)
        self.positions = [self.position]
        self.last = None
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def draw(self):
        """Метод отрисовки змейки"""
        # Отрисовка сегментов змейки
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод изменения направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод получения позиции головы змейки"""
        return self.positions[0]

    def move(self):
        """Метод обработки изменения позиции головы змейки"""
        head_position = self.get_head_position()
        new_head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.position = new_head_position
        self.positions.insert(0, new_head_position)

    def reset(self):
        """Метод сброса прогресса змейки"""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(game_object):
    """Функция обработки нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            game_object.next_direction = DIRECTIONS.get(
                (event.key, game_object.direction), game_object.direction
            )
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def main():
    """Главная функция"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    ssnake = Snake()
    the_fruit = Apple()
    while the_fruit.position in ssnake.positions:
        the_fruit.randomize_position()

    while True:
        clock.tick(SPEED)

        handle_keys(ssnake)
        ssnake.update_direction()
        ssnake.move()
        if ssnake.positions[0] != the_fruit.position:
            ssnake.last = ssnake.positions[-1]
            ssnake.positions.pop()
        else:
            ssnake.last = None
            ssnake.length += 1
            the_fruit.randomize_position()
            while the_fruit.position in ssnake.positions:
                the_fruit.randomize_position()
        if ssnake.positions[0] in ssnake.positions[1:]:
            ssnake.reset()
        screen.fill(BOARD_BACKGROUND_COLOR)
        ssnake.draw()
        the_fruit.draw()
        pygame.display.update()


if __name__ == "__main__":
    """Запуск программы"""
    main()

# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
