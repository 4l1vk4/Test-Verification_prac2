from typing import List, Union

Number = Union[int, float]
Matrix = List[List[Number]]
Vector = List[Number]


def matrix_addition(a: Matrix, b: Matrix) -> Matrix:
    if not a or not b or not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("Матрицы должны быть непустыми списками строк.")

    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])

    if rows_a != rows_b or cols_a != cols_b:
        raise ValueError(
            f"Несовпадение размерностей для сложения: ({rows_a}x{cols_a}) и ({rows_b}x{cols_b})."
        )

    for r in a:
        if len(r) != cols_a:
            raise ValueError("Матрица A не является прямоугольной.")
    for r in b:
        if len(r) != cols_b:
            raise ValueError("Матрица B не является прямоугольной.")

    return [
        [round(a[i][j] + b[i][j], 4) for j in range(cols_a)]
        for i in range(rows_a)
    ]


def matrix_multiplication(a: Matrix, b: Matrix) -> Matrix:
    if not a or not b or not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("Матрицы должны быть непустыми списками строк.")

    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])

    if cols_a != rows_b:
        raise ValueError(
            f"Размерности не согласованы для умножения: число столбцов A ({cols_a}) != числу строк B ({rows_b})."
        )

    for r in a:
        if len(r) != cols_a:
            raise ValueError("Матрица A не является прямоугольной.")
    for r in b:
        if len(r) != cols_b:
            raise ValueError("Матрица B не является прямоугольной.")

    res = [[0.0 for _ in range(cols_b)] for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            s = sum(a[i][k] * b[k][j] for k in range(cols_a))
            res[i][j] = round(s, 4)

    return res


def matrix_transpose(a: Matrix) -> Matrix:
    if not a or not isinstance(a, list):
        raise ValueError("Матрица должна быть непустым списком строк.")

    rows, cols = len(a), len(a[0])
    for r in a:
        if len(r) != cols:
            raise ValueError("Матрица не является прямоугольной.")

    return [[a[i][j] for i in range(rows)] for j in range(cols)]


def matrix_determinant(a: Matrix) -> float:
    if not a or not isinstance(a, list):
        raise ValueError("Матрица должна быть непустым списком.")

    n = len(a)
    for r in a:
        if len(r) != n:
            raise ValueError(
                "Определитель вычисляется только для квадратных матриц."
            )

    if n == 1:
        return round(float(a[0][0]), 4)
    if n == 2:
        return round(float(a[0][0] * a[1][1] - a[0][1] * a[1][0]), 4)

    det = 0.0
    for j in range(n):
        sub_matrix = [row[:j] + row[j + 1 :] for row in a[1:]]
        sign = 1.0
        det += sign * a[0][j] * matrix_determinant(sub_matrix)

    return round(det, 4)


def vector_dot_product(u: Vector, v: Vector) -> float:
    if not isinstance(u, list) or not isinstance(v, list):
        raise TypeError("Векторы должны быть списками чисел.")
    if len(u) == 0 or len(v) == 0:
        raise ValueError("Векторы не должны быть пустыми.")
    if len(u) != len(v):
        raise ValueError(
            f"Размерности векторов не совпадают: {len(u)} != {len(v)}."
        )

    dot = sum(x * y for x, y in zip(u, v))
    return round(float(dot), 4)
