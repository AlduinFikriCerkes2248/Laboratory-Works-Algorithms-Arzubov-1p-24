import math

def knapsack_dp(W, weights, values, n):
    K = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif weights[i-1] <= w:
                K[i][w] = max(values[i-1] + K[i-1][w - weights[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
    return K[n][W]

def knapsack_greedy(W, weights, values, n):
    items = []
    for i in range(n):
        ratio = values[i] / weights[i]
        items.append((values[i], weights[i], i, ratio))
    items.sort(key=lambda x: x[3], reverse=True)
    total_value = 0
    current_weight = 0
    for item in items:
        val, wt, index, ratio = item
        if current_weight + wt <= W:
            current_weight += wt
            total_value += val
    return total_value

def max_heapify(A, i, heap_size):
    l = 2 * i + 1
    r = 2 * i + 2
    largest = i
    if l < heap_size and A[l][1] > A[i][1]:
        largest = l
    if r < heap_size and A[r][1] > A[largest][1]:
        largest = r
    if largest != i:
        A[i], A[largest] = A[largest], A[i]
        max_heapify(A, largest, heap_size)

def build_max_heap(A):
    heap_size = len(A)
    for i in range(len(A)//2 - 1, -1, -1):
        max_heapify(A, i, heap_size)
    return heap_size

def heap_sort(A):
    heap_size = build_max_heap(A)
    for i in range(len(A)-1, 0, -1):
        A[0], A[i] = A[i], A[0]
        heap_size -= 1
        max_heapify(A, 0, heap_size)

def activity_selection_greedy(activities):
    heap_sort(activities)
    n = len(activities)
    selected = []
    i = 0
    selected.append(activities[i])
    for j in range(1, n):
        if activities[j][0] >= activities[i][1]:
            selected.append(activities[j])
            i = j
    return selected

def activity_selection_dp(activities):
    heap_sort(activities)
    n = len(activities)
    L = [1] * n
    for i in range(1, n):
        for j in range(i):
            if activities[j][1] <= activities[i][0] and L[i] < L[j] + 1:
                L[i] = L[j] + 1
    return max(L) if L else 0

def kadane_1d(arr):
    max_so_far = float('-inf')
    current_max = 0
    start = end = s = 0
    for i in range(len(arr)):
        current_max += arr[i]
        if max_so_far < current_max:
            max_so_far = current_max
            start = s
            end = i
        if current_max < 0:
            current_max = 0
            s = i + 1
    return max_so_far, start, end

def kadane_2d_astronomy(matrix):
    ROWS = len(matrix)
    COLS = len(matrix[0]) if ROWS > 0 else 0
    max_brightness = float('-inf')
    final_top = final_bottom = final_left = final_right = 0
    for left in range(COLS):
        temp = [0] * ROWS
        for right in range(left, COLS):
            for i in range(ROWS):
                temp[i] += matrix[i][right]
            curr_max, start_row, end_row = kadane_1d(temp)
            if curr_max > max_brightness:
                max_brightness = curr_max
                final_left = left
                final_right = right
                final_top = start_row
                final_bottom = end_row
    return max_brightness, (final_top, final_left), (final_bottom, final_right)

def get_extras(words, i, j, L):
    length = sum(len(words[k]) for k in range(i, j + 1))
    length += (j - i)
    return L - length

def text_justification_dp(words, L):
    n = len(words)
    extras = [[0]*n for _ in range(n)]
    lc = [[0]*n for _ in range(n)]
    c = [0]*(n+1)
    p = [0]*(n+1)
    for i in range(n):
        for j in range(i, n):
            extras[i][j] = get_extras(words, i, j, L)
            if extras[i][j] < 0:
                lc[i][j] = float('inf')
            else:
                lc[i][j] = extras[i][j] ** 3
    for j in range(1, n+1):
        c[j] = float('inf')
        for i in range(1, j+1):
            if c[i-1] != float('inf') and lc[i-1][j-1] != float('inf'):
                if c[i-1] + lc[i-1][j-1] < c[j]:
                    c[j] = c[i-1] + lc[i-1][j-1]
                    p[j] = i
    lines = []
    curr = n
    while curr > 0:
        start = p[curr] - 1
        lines.append(" ".join(words[start:curr]))
        curr = p[curr] - 1
    lines.reverse()
    return c[n], lines

def text_justification_greedy(words, L):
    lines = []
    current_line = []
    current_length = 0
    cost = 0
    for word in words:
        if current_length + len(word) + len(current_line) <= L:
            current_line.append(word)
            current_length += len(word)
        else:
            spaces_left = L - (current_length + len(current_line) - 1)
            cost += spaces_left ** 3
            lines.append(" ".join(current_line))
            current_line = [word]
            current_length = len(word)
    if current_line:
        spaces_left = L - (current_length + len(current_line) - 1)
        cost += spaces_left ** 3
        lines.append(" ".join(current_line))
    return cost, lines

if __name__ == "__main__":
    print("=== ТЕМА 5: РЮКЗАК 0-1 ===")
    val = [60, 100, 120]
    wt = [10, 20, 30]
    W = 50
    n = len(val)
    print(f"Максимальна цінність (ДП): {knapsack_dp(W, wt, val, n)}")
    print(f"Максимальна цінність (Жадібний): {knapsack_greedy(W, wt, val, n)}")
    print("*(Жадібний підхід може давати неоптимальний результат залежно від даних)*\n")

    print("=== ТЕМА 6.1: ПЛАНУВАННЯ РОБІТ (HEAP SORT ВАРІАНТ 1) ===")
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 8), (5, 9), (6, 10), (8, 11), (8, 12), (2, 13), (12, 14)]
    greedy_res = activity_selection_greedy(activities.copy())
    dp_res = activity_selection_dp(activities.copy())
    print(f"Жадібний підхід обрав робіт: {len(greedy_res)} -> {greedy_res}")
    print(f"ДП алгоритм вирахував макс сумісних робіт: {dp_res}\n")

    print("=== ТЕМА 6.2: АЛГОРИТМ КАДАНЕ 2D (Астрономічне зображення) ===")
    astro_image = [
        [-1, -2, -1,  4, -1],
        [-2, -3,  2,  5, -2],
        [-3,  1,  3,  4, -1],
        [ 2, -1, -2, -3, -5]
    ]
    max_bright, top_left, bottom_right = kadane_2d_astronomy(astro_image)
    print(f"Найвища сумарна яскравість області: {max_bright}")
    print(f"Координати (Top-Left): {top_left}, (Bottom-Right): {bottom_right}\n")

    print("=== ТЕМА 6.3: ВИРІВНЮВАННЯ ТЕКСТУ ===")
    LINE_LENGTH = 21
    text = "This is a sample text designed to demonstrate the text justification problem using both greedy and dynamic programming approaches to see the difference in total cost when formatting lines evenly."
    words_list = text.split()
    print(f"Слів у тексті: {len(words_list)}. Довжина рядка: {LINE_LENGTH}")
    cost_greedy, lines_greedy = text_justification_greedy(words_list, LINE_LENGTH)
    cost_dp, lines_dp = text_justification_dp(words_list, LINE_LENGTH)
    print(f"\n--- Жадібний підхід (Cost: {cost_greedy}) ---")
    for row in lines_greedy:
        print(f"'{row}' (залишок: {LINE_LENGTH - len(row)})")
    print(f"\n--- ДП підхід (Cost: {cost_dp}) ---")
    for row in lines_dp:
        print(f"'{row}' (залишок: {LINE_LENGTH - len(row)})")
    print("\n*Зробив Арзубов.М.*")
