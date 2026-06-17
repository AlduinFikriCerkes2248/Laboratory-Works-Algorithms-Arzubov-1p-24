import time
import random
import math
import matplotlib.pyplot as plt

def shell_sort(A):
    d = len(A) // 2
    while d >= 1:
        for i in range(d, len(A)):
            j = i
            while (j >= d) and (A[j - d] > A[j]):
                A[j], A[j - d] = A[j - d], A[j]
                j = j - d
        d = d // 2

def run_shell_sort_analysis():
    print("--- Тема 1.1: Аналіз Сортування Шелла (Варіант 1) ---")
    sizes = [1000, 3000, 5000, 10000, 15000, 20000, 30000]
    times = []
    print(f"{'Кількість елементів (N)':<25} | {'Час виконання (секунди)':<25}")
    print("-" * 55)
    for size in sizes:
        arr = [random.randint(1, 100000) for _ in range(size)]
        start_time = time.time()
        shell_sort(arr)
        end_time = time.time()
        exec_time = end_time - start_time
        times.append(exec_time)
        print(f"{size:<25} | {exec_time:<25.6f}")

    plt.figure(figsize=(8, 4))
    plt.plot(sizes, times, marker='o', color='g', linestyle='-', linewidth=2)
    plt.title("Залежність часу виконання Shell Sort від N (Варіант 1)")
    plt.xlabel("Кількість елементів (N)")
    plt.ylabel("Час виконання (сек)")
    plt.grid(True)
    print("\n[Закрийте вікно графіка сортування, щоб перейти до введення точок]")
    plt.show()

def get_side(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def brute_force_convex_hull(points):
    n = len(points)
    if n < 3: 
        return points
    hull = []
    for i in range(n):
        for j in range(n):
            if i == j: 
                continue
            all_on_one_side = True
            expected_sign = 0
            for k in range(n):
                if k == i or k == j: 
                    continue
                side = get_side(points[i], points[j], points[k])
                if abs(side) > 1e-9:
                    if expected_sign == 0:
                        expected_sign = 1 if side > 0 else -1
                    elif (side > 0 and expected_sign == -1) or (side < 0 and expected_sign == 1):
                        all_on_one_side = False
                        break
            if all_on_one_side:
                if points[i] not in hull: hull.append(points[i])
                if points[j] not in hull: hull.append(points[j])
                
    if len(hull) > 0:
        cx = sum(p[0] for p in hull) / len(hull)
        cy = sum(p[1] for p in hull) / len(hull)
        hull.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    return hull

def jarvis_march(points):
    n = len(points)
    if n < 3: 
        return points
    start = min(points, key=lambda p: p[0])
    hull = []
    p = start
    while True:
        hull.append(p)
        q = points[0]
        for r in points:
            if r == p: 
                continue
            if q == p or get_side(p, q, r) > 0:
                q = r
        p = q
        if p == start: 
            break
    return hull

def graham_scan(points):
    if len(points) < 3: 
        return points
    start = min(points, key=lambda p: (p[1], p[0]))
    
    def algo_key(p):
        angle = math.atan2(p[1] - start[1], p[0] - start[0])
        dist = math.hypot(p[1] - start[1], p[0] - start[0])
        return (angle, dist)
    
    sorted_pts = sorted(points, key=algo_key)
    hull = [sorted_pts[0], sorted_pts[1]]
    for p in sorted_pts[2:]:
        while len(hull) > 1 and get_side(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull

def show_convex_hull_plot(points, hull_points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    plt.figure(figsize=(7, 7))
    plt.scatter(x_coords, y_coords, color='blue', label='Точки множини', zorder=5, s=50)
    if len(hull_points) > 0:
        hull_plot = hull_points + [hull_points[0]]
        hx = [p[0] for p in hull_plot]
        hy = [p[1] for p in hull_plot]
        plt.plot(hx, hy, color='red', linewidth=2, label='Опукла оболонка', zorder=4)
        plt.scatter(hx, hy, color='red', zorder=6, s=60)
    plt.title('Опукла оболонка (Метод грубої сили за методичкою)')
    plt.xlabel('Вісь X')
    plt.ylabel('Вісь Y')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()

N_KNIGHT = 5

def is_valid_knight(i, j, sol):
    return 1 <= i <= N_KNIGHT and 1 <= j <= N_KNIGHT and sol[i-1][j-1] == -1

def knight_tour(sol, i, j, step_count, x_move, y_move):
    if step_count == N_KNIGHT * N_KNIGHT:
        return True
    for k in range(8):
        next_i = i + x_move[k]
        next_j = j + y_move[k]
        if is_valid_knight(next_i, next_j, sol):
            sol[next_i-1][next_j-1] = step_count
            if knight_tour(sol, next_i, next_j, step_count + 1, x_move, y_move):
                return True
            sol[next_i-1][next_j-1] = -1
    return False

def start_knight_tour():
    print("\n--- Тема 2.3: Задача про хід коня ---")
    sol = [[-1 for _ in range(N_KNIGHT)] for _ in range(N_KNIGHT)]
    x_move = [2, 1, -1, -2, -2, -1, 1, 2]
    y_move = [1, 2, 2, 1, -1, -2, -2, -1]
    sol[0][0] = 0
    if knight_tour(sol, 1, 1, 1, x_move, y_move):
        for row in sol:
            print(" ".join(f"{x:2d}" for x in row))
    else:
        print("Розв'язку не існує")

def is_safe_sudoku(grid, row, col, digit):
    for x in range(9):
        if grid[row][x] == digit or grid[x][col] == digit:
            return False
    start_r, start_c = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + start_r][j + start_c] == digit:
                return False
    return True

def sudoku_solver(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for digit in range(1, 10):
                    if is_safe_sudoku(grid, row, col, digit):
                        grid[row][col] = digit
                        if sudoku_solver(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def run_sudoku_demo():
    print("\n--- Тема 2.4: Розв'язувач Судоку ---")
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    if sudoku_solver(grid):
        for r in grid: 
            print(r)

N_MAZE = 4
def is_valid_maze(maze, i, j):
    return 0 <= i <= N_MAZE-1 and 0 <= j <= N_MAZE-1 and maze[i][j] == 1

def find_maze_path(maze, x, y, sol):
    if x == N_MAZE-1 and y == N_MAZE-1:
        sol[x][y] = 1
        return True
    if is_valid_maze(maze, x, y):
        sol[x][y] = 1
        if find_maze_path(maze, x + 1, y, sol): return True
        if find_maze_path(maze, x, y + 1, sol): return True
        sol[x][y] = 0
        return False
    return False

def solve_maze_demo():
    print("\n--- Тема 2.5: Алгоритм виходу з лабіринту ---")
    maze = [
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 1, 0, 0],
        [1, 1, 1, 1]
    ]
    sol = [[0]*N_MAZE for _ in range(N_MAZE)]
    if find_maze_path(maze, 0, 0, sol):
        for r in sol: 
            print(r)
    else:
        print("Розв'язку не існує")

if __name__ == "__main__":
    run_shell_sort_analysis()
    
    print("\nВведіть координати точок у форматі (X Y). Для завершення натисніть Enter на порожньому рядку.")
    pts = []
    while True:
        user_input = input(f"Точка {len(pts) + 1}: ")
        if not user_input.strip():
            break
        try:
            x, y = map(float, user_input.split())
            pts.append((x, y))
        except ValueError:
            print("Помилка вводу! Системи координат мають бути розділені пробілом (наприклад: 1.5 2)")

    if len(pts) < 3:
        print("\nПомилка: Введено менше 3 точок. Розрахунок оболонки неможливий.")
    else:
        print(f"\nЗадані точки: {pts}")
        
        print("\n--- Тема 1.2: Опукла оболонка (Повний перебір) ---")
        hull_res = brute_force_convex_hull(pts)
        print("Результат:", hull_res)
        
        print("\n--- Тема 2.1: Опукла оболонка (Джарвіс) ---")
        print("Результат:", jarvis_march(pts))
        
        print("\n--- Тема 2.2: Опукла оболонка (Грехем) ---")
        print("Результат:", graham_scan(pts))
        
        start_knight_tour()
        run_sudoku_demo()
        solve_maze_demo()
        
        show_convex_hull_plot(pts, hull_res)
        
        print("\nЗробив Арзубов.М.")
