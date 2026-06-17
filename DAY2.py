import math
import time
import random

def size10(num):
    if num == 0:
        return 1
    return int(math.log10(abs(num))) + 1

def split_at(num, m2):
    power = 10 ** m2
    low = num % power
    high = num // power
    return high, low

def karatsuba(A, B):
    if A < 10 or B < 10:
        return A * B
    m = min(size10(A), size10(B))
    m2 = math.floor(m / 2)
    high1, low1 = split_at(A, m2)
    high2, low2 = split_at(B, m2)
    z0 = karatsuba(low1, low2)
    z1 = karatsuba(low1 + high1, low2 + high2)
    z2 = karatsuba(high1, high2)
    return (z2 * (10 ** (m2 * 2))) + ((z1 - z2 - z0) * (10 ** m2)) + z0

def naive_multiply(A, B):
    return A * B

def merge(A, p, q, r):
    n1 = q - p + 1
    n2 = r - q
    L = [0] * (n1 + 2)
    R = [0] * (n2 + 2)
    for i in range(1, n1 + 1):
        L[i] = A[(p + i - 1) - 1]
    for j in range(1, n2 + 1):
        R[j] = A[(q + j) - 1]
    L[n1 + 1] = float('inf')
    R[n2 + 1] = float('inf')
    i = 1
    j = 1
    for k in range(p, r + 1):
        if L[i] <= R[j]:
            A[k - 1] = L[i]
            i = i + 1
        else:
            A[k - 1] = R[j]
            j = j + 1

def merge_sort(A, p, r):
    if p < r:
        q = (p + r) // 2
        merge_sort(A, p, q)
        merge_sort(A, q + 1, r)
        merge(A, p, q, r)

def counting_sort(A, B, k):
    C = [0] * (k + 1)
    for i in range(0, k + 1):
        C[i] = 0
    for j in range(1, len(A) + 1):
        C[A[j - 1]] += 1
    for i in range(1, k + 1):
        C[i] = C[i] + C[i - 1]
    for j in range(len(A), 0, -1):
        B[C[A[j - 1]] - 1] = A[j - 1]
        C[A[j - 1]] -= 1

if __name__ == "__main__":
    print("=== ТЕМА 3: МНОЖЕННЯ КАРАЦУБИ ===")
    n_digits = 50
    num1 = int("".join([str(random.randint(1, 9)) for _ in range(n_digits)]))
    num2 = int("".join([str(random.randint(1, 9)) for _ in range(n_digits)]))
    
    t0 = time.perf_counter()
    res_naive = naive_multiply(num1, num2)
    t1 = time.perf_counter()
    
    t2 = time.perf_counter()
    res_karatsuba = karatsuba(num1, num2)
    t3 = time.perf_counter()
    
    print(f"Довжина чисел: {n_digits} знаків.")
    print(f"Час наївного множення: {(t1 - t0):.8f} сек.")
    print(f"Час множення Карацуби: {(t3 - t2):.8f} сек.")
    print(f"Результати збігаються: {res_naive == res_karatsuba}\n")

    print("=== ТЕМА 3: СОРТУВАННЯ ЗЛИТТЯМ ===")
    test_array_merge = [random.randint(1, 100) for _ in range(10)]
    print("Вхідний масив: ", test_array_merge)
    merge_sort(test_array_merge, 1, len(test_array_merge))
    print("Відсортований масив:", test_array_merge, "\n")

    print("=== ТЕМА 4: СОРТУВАННЯ ПІДРАХУНКОМ ===")
    test_array_counting = [2, 5, 3, 0, 2, 3, 0, 3]
    k_max = max(test_array_counting)
    output_array = [0] * len(test_array_counting)
    
    print("Вхідний масив A:      ", test_array_counting)
    counting_sort(test_array_counting, output_array, k_max)
    print("Відсортований масив B:", output_array)
    
    print("\n*Зробив Арзубов.М.*")
