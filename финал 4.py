import random
import os

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from PIL import Image


HEALTHY = 0

SICK_1 = 1
SICK_2 = 2
SICK_3 = 3
SICK_4 = 4

DEAD = 5
IMMUNE = 6

LAST_SICK_STATE = SICK_4

SAVE_FRAMES = True
FRAMES_FOLDER = "конец4"


def get_integer(text, min_value, max_value=None):
    while True:
        try:
            value = int(input(text))

            if value < min_value:
                print("Число слишком маленькое.")
                continue

            if max_value is not None and value > max_value:
                print("Число слишком большое.")
                continue

            return value

        except ValueError:
            print("Ошибка. Нужно ввести целое число.")


def get_float(text, min_value, max_value):
    while True:
        try:
            value_text = input(text).replace(",", ".")
            value = float(value_text)

            if value < min_value or value > max_value:
                print("Введите число от", min_value, "до", max_value)
                continue

            return value

        except ValueError:
            print("Ошибка. Нужно ввести число.")


def get_settings():
    print()
    print("Настройка модели эпидемии")
    print("-" * 50)

    width = get_integer(
        "Количество клеток по горизонтали: ",
        1
    )

    height = get_integer(
        "Количество клеток по вертикали: ",
        1
    )

    min_sick_neighbors = get_integer(
        "Минимальное количество больных соседей "
        "для заражения от 1 до 8: ",
        1,
        8
    )

    death_percent = get_float(
        "Вероятность смерти на второй стадии "
        "в процентах от 0 до 100: ",
        0,
        100
    )

    infected_percent = get_float(
        "Процент заражённых клеток в начале "
        "от 0 до 100: ",
        0,
        100
    )

    delay = get_float(
        "Длительность дня в секундах: ",
        0,
        1000
    )

    print("-" * 50)
    print("Настройки приняты.")
    print()

    return (
        width,
        height,
        min_sick_neighbors,
        death_percent / 100,
        infected_percent,
        delay
    )


def create_grid(width, height):
    return [
        [HEALTHY for _ in range(width)]
        for _ in range(height)
    ]


def get_neighbors(x, y, width, height):
    neighbors = []

    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dx == 0 and dy == 0:
                continue

            neighbor_x = x + dx
            neighbor_y = y + dy

            if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
                neighbors.append((neighbor_x, neighbor_y))

    return neighbors


def has_sick_cells(grid):
    for row in grid:
        for state in row:
            if SICK_1 <= state <= LAST_SICK_STATE:
                return True

    return False


def update_grid(
    grid,
    width,
    height,
    min_sick_neighbors,
    death_probability
):
    new_grid = [row.copy() for row in grid]

    for y in range(height):
        for x in range(width):
            state = grid[y][x]

            if state == DEAD:
                new_grid[y][x] = DEAD

            elif state == IMMUNE:
                new_grid[y][x] = IMMUNE

            elif state == HEALTHY:
                sick_count = 0

                for neighbor_x, neighbor_y in get_neighbors(
                    x,
                    y,
                    width,
                    height
                ):
                    neighbor_state = grid[neighbor_y][neighbor_x]

                    if SICK_1 <= neighbor_state <= LAST_SICK_STATE:
                        sick_count += 1

                if sick_count >= min_sick_neighbors:
                    new_grid[y][x] = SICK_1

            elif state == SICK_1:
                new_grid[y][x] = SICK_2

            elif state == SICK_2:
                if random.random() < death_probability:
                    new_grid[y][x] = DEAD
                else:
                    new_grid[y][x] = SICK_3

            elif state == SICK_3:
                new_grid[y][x] = SICK_4

            elif state == SICK_4:
                new_grid[y][x] = IMMUNE

    return new_grid


def infect_initial_cells(grid, width, height, infected_percent):
    total_cells = width * height
    infected_count = int(total_cells * infected_percent / 100)

    infected_cells = random.sample(
        range(total_cells),
        infected_count
    )

    for number in infected_cells:
        x = number % width
        y = number // width
        grid[y][x] = SICK_1


def get_statistics(grid):
    healthy_count = 0
    sick_count = 0
    dead_count = 0
    immune_count = 0

    for row in grid:
        for state in row:
            if state == HEALTHY:
                healthy_count += 1
            elif SICK_1 <= state <= LAST_SICK_STATE:
                sick_count += 1
            elif state == DEAD:
                dead_count += 1
            elif state == IMMUNE:
                immune_count += 1

    return (
        healthy_count,
        sick_count,
        dead_count,
        immune_count
    )


def print_day_statistics(day, grid):
    healthy, sick, dead, immune = get_statistics(grid)

    print()
    print("=" * 50)
    print(f"ДЕНЬ {day} ЭПИДЕМИИ")
    print("=" * 50)
    print("Здоровых клеток:", healthy)
    print("Больных клеток:", sick)
    print("Умерших клеток:", dead)
    print("Иммунных клеток:", immune)
    print("=" * 50)


def create_color_map():
    colors = [
        "#66bb6a",
        "#e53935",
        "#ff7043",
        "#ff9800",
        "#ffcc80",
        "#000000",
        "#7FFF00"
    ]

    return ListedColormap(colors)


def draw_grid(
    image,
    grid,
    step,
    infected_percent,
    min_sick_neighbors
):
    healthy, sick, dead, immune = get_statistics(grid)

    image.set_data(grid)

    image.axes.set_title(
        "Эпидемия\n"
        f"Для заражения нужно соседей: "
        f"{min_sick_neighbors}\n"
        f"Начально заражено: "
        f"{infected_percent:.2f}%\n"
        f"Шаг: {step}\n"
        f"Здоровых: {healthy} | "
        f"Больных: {sick} | "
        f"Умерших: {dead} | "
        f"Переболевших: {immune}"
    )


def delete_old_frames():
    os.makedirs(FRAMES_FOLDER, exist_ok=True)

    for file_name in os.listdir(FRAMES_FOLDER):
        if file_name.endswith(".png"):
            file_path = os.path.join(
                FRAMES_FOLDER,
                file_name
            )
            os.remove(file_path)


def create_gif(delay):
    if not SAVE_FRAMES:
        print("Сохранение кадров выключено.")
        return

    frame_files = []

    for file_name in os.listdir(FRAMES_FOLDER):
        if file_name.endswith(".png"):
            frame_files.append(
                os.path.join(FRAMES_FOLDER, file_name)
            )

    frame_files.sort()

    if not frame_files:
        print("Кадры не найдены.")
        return

    frames = []

    for file_name in frame_files:
        frame = Image.open(file_name).convert("RGB")
        frames.append(frame)

    gif_path = os.path.join(
        FRAMES_FOLDER,
        "epidemic.gif"
    )

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(delay * 1000),
        loop=0
    )

    for frame in frames:
        frame.close()

    print("GIF сохранён:", gif_path)


def show_last_day(
    last_grid,
    last_step,
    color_map
):
    figure, axis = plt.subplots(
        figsize=(10, 7)
    )

    image = axis.imshow(
        last_grid,
        cmap=color_map,
        vmin=HEALTHY,
        vmax=IMMUNE,
        interpolation="nearest"
    )

    axis.set_title(
        f"Последний день эпидемии: {last_step}"
    )
    axis.set_aspect("equal")
    axis.set_xlabel("")
    axis.set_ylabel("")

    figure.colorbar(
        image,
        ax=axis,
        label="Состояние клетки"
    )

    figure.tight_layout()
    figure.canvas.draw()
    figure.canvas.flush_events()


def main():
    settings = get_settings()

    width = settings[0]
    height = settings[1]
    min_sick_neighbors = settings[2]
    death_probability = settings[3]
    infected_percent = settings[4]
    delay = settings[5]

    if SAVE_FRAMES:
        delete_old_frames()

    grid = create_grid(width, height)

    infect_initial_cells(
        grid,
        width,
        height,
        infected_percent
    )

    first_grid = [row.copy() for row in grid]

    print_day_statistics(1, grid)

    plt.ion()

    figure, axis = plt.subplots(figsize=(10, 8))

    color_map = create_color_map()

    image = axis.imshow(
        grid,
        cmap=color_map,
        vmin=HEALTHY,
        vmax=IMMUNE,
        interpolation="nearest"
    )

    axis.set_xlabel("")
    axis.set_ylabel("")
    axis.set_aspect("equal")

    colorbar = figure.colorbar(image, ax=axis)
    colorbar.set_label("Состояние клетки")

    step = 0

    while has_sick_cells(grid):
        draw_grid(
            image,
            grid,
            step,
            infected_percent,
            min_sick_neighbors
        )

        figure.canvas.draw()
        figure.canvas.flush_events()

        if SAVE_FRAMES:
            file_name = os.path.join(
                FRAMES_FOLDER,
                f"step_{step:03d}.png"
            )

            figure.savefig(
                file_name,
                dpi=150,
                bbox_inches="tight"
            )

        plt.pause(delay)

        grid = update_grid(
            grid,
            width,
            height,
            min_sick_neighbors,
            death_probability
        )

        step += 1

    draw_grid(
        image,
        grid,
        step,
        infected_percent,
        min_sick_neighbors
    )

    figure.canvas.draw()
    figure.canvas.flush_events()

    if SAVE_FRAMES:
        final_file_name = os.path.join(
            FRAMES_FOLDER,
            f"step_{step:03d}.png"
        )

        figure.savefig(
            final_file_name,
            dpi=150,
            bbox_inches="tight"
        )

    plt.pause(delay)

    print_day_statistics(step + 1, grid)

    print()
    print("=" * 50)
    print("ЭПИДЕМИЯ ЗАВЕРШИЛАСЬ")
    print("=" * 50)
    print("Последний день эпидемии:", step + 1)
    print("=" * 50)


    show_last_day(
    grid,
    step + 1,
    color_map
    )

    plt.ioff()

    create_gif(delay)

    plt.show()

100
if __name__ == "__main__":
    main()