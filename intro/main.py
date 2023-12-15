import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
width, height = 800, 600

# Цвета
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Инициализация окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Простой платформер")

# Инициализация часов
clock = pygame.time.Clock()

# Размеры кружка
circle_radius = 25

# Создание объекта для кружка
circle_x = (width - circle_radius) // 2
circle_y = (height - circle_radius) // 2
circle = pygame.Rect(circle_x, circle_y, circle_radius * 2, circle_radius * 2)

# Вектор скорости для броска
throw_velocity = pygame.math.Vector2(0, 0)

# Гравитация
gravity = pygame.math.Vector2(0, 0.5)

# Список для хранения координат маршрута
route_points = []

# Текущие координаты мыши
mouse_x, mouse_y = 0, 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Проверка, была ли нажата левая кнопка мыши в области кружка
            if circle.collidepoint(event.pos):
                throw_velocity = pygame.math.Vector2(0, 0)  # Сброс вектора скорости при поднятии мяча
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Завершение броска кружка
            throw_velocity = pygame.math.Vector2((event.pos[0] - circle.centerx) / 20, (event.pos[1] - circle.centery) / 20)
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos  # Обновление координат мыши
            route_points.append((mouse_x, mouse_y))  # Добавление текущей позиции мыши в список маршрута

    # Применение гравитации при броске
    throw_velocity += gravity

    # Обновление позиции кружка в соответствии с вектором скорости
    circle.x += throw_velocity.x
    circle.y += throw_velocity.y

    # Проверка, чтобы кружок не уходил за пределы экрана
    if circle.y > height - circle_radius * 2:
        circle.y = height - circle_radius * 2
        throw_velocity.y = -throw_velocity.y * 0.7  # Отскок от нижней границы с потерей энергии

    if circle.x < 0 or circle.x > width - circle_radius * 2:
        throw_velocity.x = -throw_velocity.x * 0.7  # Отскок от боковых границ с потерей энергии

    # Заливка экрана черным цветом
    screen.fill(black)

    # Отрисовка кружка на экране
    pygame.draw.circle(screen, red, circle.center, circle_radius)

    # Предсказание траектории и отрисовка маршрута
    if throw_velocity.length() > 0:
        predicted_points = []
        for t in range(100):
            position = circle.center + throw_velocity * t + 0.5 * gravity * t**2
            predicted_points.append(position)
        pygame.draw.lines(screen, white, False, predicted_points, 2)

   

    # Обновление экрана
    pygame.display.flip()

    # Задержка для контроля частоты кадров
    clock.tick(60)
