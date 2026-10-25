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
FRAMES_FOLDER = "испр4"
GRAPH_FRAMES_FOLDER = "график4"


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

    immunity_days = get_integer(
        "Количество дней иммунитета: ",
        1
    )

    days_count = get_integer(
        "Количество дней эпидемии: ",
        1
    )

    delay = get_float(
        "Пауза между кадрами в секундах: ",
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
        immunity_days,
        days_count,
        delay
    )


def create_grid(width, height):
    return [
        [HEALTHY for _ in range(width)]
        for _ in range(height)
    ]


def create_immunity_grid(width, height):
    return [
        [0 for _ in range(width)]
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


def update_grid(
    grid,
    immunity_grid,
    width,
    height,
    min_sick_neighbors,
    death_probability,
    immunity_days
):
    new_grid = [row.copy() for row in grid]
    new_immunity_grid = [row.copy() for row in immunity_grid]

    for y in range(height):
        for x in range(width):
            state = grid[y][x]

            if state == DEAD:
                new_grid[y][x] = DEAD
                new_immunity_grid[y][x] = 0

            elif state == IMMUNE:
                # Каждый день иммунитета уменьшается на 1.
                new_immunity_grid[y][x] -= 1

                # После окончания иммунитета клетка снова становится здоровой.
                if new_immunity_grid[y][x] <= 0:
                    new_grid[y][x] = HEALTHY
                    new_immunity_grid[y][x] = 0
                else:
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
                    new_immunity_grid[y][x] = 0
                else:
                    new_grid[y][x] = SICK_3

            elif state == SICK_3:
                new_grid[y][x] = SICK_4

            elif state == SICK_4:
                # После последней стадии болезни клетка получает иммунитет.
                new_grid[y][x] = IMMUNE
                new_immunity_grid[y][x] = immunity_days

    return new_grid, new_immunity_grid


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
    day,
    days_count,
    infected_percent,
    min_sick_neighbors,
    immunity_days
):
    healthy, sick, dead, immune = get_statistics(grid)

    image.set_data(grid)

    image.axes.set_title(
        "Эпидемия\n"
        f"Для заражения нужно соседей: "
        f"{min_sick_neighbors}\n"
        f"Начально заражено: "
        f"{infected_percent:.2f}%\n"
        f"Иммунитет: {immunity_days} дн.\n"
        f"День: {day} из {days_count}\n"
        f"Здоровых: {healthy} | "
        f"Больных: {sick} | "
        f"Умерших: {dead} | "
        f"Иммунных: {immune}"
    )


def delete_old_frames(folder):
    os.makedirs(folder, exist_ok=True)

    for file_name in os.listdir(folder):
        if file_name.endswith(".png"):
            file_path = os.path.join(folder, file_name)
            os.remove(file_path)


def create_gif(folder, gif_name, delay):
    if not SAVE_FRAMES:
        print("Сохранение кадров выключено.")
        return

    frame_files = []

    for file_name in os.listdir(folder):
        if file_name.endswith(".png"):
            frame_files.append(
                os.path.join(folder, file_name)
            )

    frame_files.sort()

    if not frame_files:
        print("Кадры не найдены.")
        return

    frames = []

    for file_name in frame_files:
        frame = Image.open(file_name).convert("RGB")
        frames.append(frame)

    gif_path = os.path.join(folder, gif_name)

    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=max(1, int(delay * 1000)),
        loop=0
    )

    for frame in frames:
        frame.close()

    print("GIF сохранён:", gif_path)


def show_last_day(
    last_grid,
    last_day,
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
        f"Последний день эпидемии: {last_day}"
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


def save_frame(figure, day):
    if not SAVE_FRAMES:
        return

    file_name = os.path.join(
        FRAMES_FOLDER,
        f"day_{day:05d}.png"
    )

    figure.savefig(
        file_name,
        dpi=150,
        bbox_inches="tight"
    )


def draw_graph(
    axis,
    days_history,
    healthy_history,
    sick_history,
    immune_history,
    dead_history,
    days_count,
    total_cells
):
    axis.clear()

    axis.plot(
        days_history,
        sick_history,
        color="#e53935",
        linewidth=2,
        label="Заразившиеся"
    )

    axis.plot(
        days_history,
        healthy_history,
        color="#66bb6a",
        linewidth=2,
        label="Здоровые"
    )

    axis.plot(
        days_history,
        immune_history,
        color="#7FFF00",
        linewidth=2,
        label="Иммунные"
    )

    axis.plot(
        days_history,
        dead_history,
        color="#000000",
        linewidth=2,
        label="Умершие"
    )

    axis.set_title("Изменение количества клеток во время эпидемии")
    axis.set_xlabel("Количество дней эпидемии")
    axis.set_ylabel("Количество клеток")

    axis.set_xlim(1, days_count)
    axis.set_ylim(0, total_cells)

    axis.grid(True, linestyle="--", alpha=0.5)
    axis.legend(loc="best")


def save_graph_frame(figure, day):
    if not SAVE_FRAMES:
        return

    file_name = os.path.join(
        GRAPH_FRAMES_FOLDER,
        f"graph_day_{day:05d}.png"
    )

    figure.savefig(
        file_name,
        dpi=150,
        bbox_inches="tight"
    )


def main():
    settings = get_settings()

    width = settings[0]
    height = settings[1]
    min_sick_neighbors = settings[2]
    death_probability = settings[3]
    infected_percent = settings[4]
    immunity_days = settings[5]
    days_count = settings[6]
    delay = settings[7]

    if SAVE_FRAMES:
        delete_old_frames(FRAMES_FOLDER)
        delete_old_frames(GRAPH_FRAMES_FOLDER)

    grid = create_grid(width, height)
    immunity_grid = create_immunity_grid(width, height)

    infect_initial_cells(
        grid,
        width,
        height,
        infected_percent
    )

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

    graph_figure, graph_axis = plt.subplots(figsize=(12, 7))

    days_history = []
    healthy_history = []
    sick_history = []
    immune_history = []
    dead_history = []

    total_cells = width * height

    for day in range(1, days_count + 1):
        healthy, sick, dead, immune = get_statistics(grid)

        days_history.append(day)
        healthy_history.append(healthy)
        sick_history.append(sick)
        immune_history.append(immune)
        dead_history.append(dead)

        draw_grid(
            image,
            grid,
            day,
            days_count,
            infected_percent,
            min_sick_neighbors,
            immunity_days
        )

        draw_graph(
            graph_axis,
            days_history,
            healthy_history,
            sick_history,
            immune_history,
            dead_history,
            days_count,
            total_cells
        )

        figure.canvas.draw()
        figure.canvas.flush_events()

        graph_figure.canvas.draw()
        graph_figure.canvas.flush_events()

        save_frame(figure, day)
        save_graph_frame(graph_figure, day)

        print(f"Рассчитано дней: {day} из {days_count}")

        if day < days_count:
            plt.pause(delay)

            grid, immunity_grid = update_grid(
                grid,
                immunity_grid,
                width,
                height,
                min_sick_neighbors,
                death_probability,
                immunity_days
            )

    plt.pause(delay)

    print_day_statistics(days_count, grid)

    print()
    print("=" * 50)
    print("РАСЧЁТ ЭПИДЕМИИ ЗАВЕРШЁН")
    print("=" * 50)
    print("Всего рассчитано дней:", days_count)
    print("=" * 50)

    show_last_day(
        grid,
        days_count,
        color_map
    )

    plt.ioff()

    create_gif(
        FRAMES_FOLDER,
        "epidemic.gif",
        delay
    )

    create_gif(
        GRAPH_FRAMES_FOLDER,
        "epidemic_graph.gif",
        delay
    )

    plt.show()


if __name__ == "__main__":
    main()