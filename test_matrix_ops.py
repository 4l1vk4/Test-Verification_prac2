import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


class TestMatrixOps(unittest.TestCase):

    def setUp(self):
        import matrix_ops

        self.mod = matrix_ops

    # --- 1. matrix_addition ---
    def test_addition_valid(self):
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        res = self.mod.matrix_addition(a, b)
        self.assertEqual(res, [[6, 8], [10, 12]])

    def test_addition_dimension_mismatch(self):
        a = [[1, 2], [3, 4]]
        b = [[1, 2, 3], [4, 5, 6]]
        with self.assertRaises(ValueError):
            self.mod.matrix_addition(a, b)

    def test_addition_invalid_input(self):
        with self.assertRaises(ValueError):
            self.mod.matrix_addition([], [[1]])
        with self.assertRaises(ValueError):
            self.mod.matrix_addition([[1, 2], [3]], [[1, 2], [3, 4]])

    # --- 2. matrix_multiplication ---
    def test_multiplication_valid(self):
        # 2x3 * 3x2 = 2x2
        a = [[1, 2, 3], [4, 5, 6]]
        b = [[7, 8], [9, 1], [2, 3]]
        # res[0][0] = 1*7 + 2*9 + 3*2 = 7 + 18 + 6 = 31
        # res[0][1] = 1*8 + 2*1 + 3*3 = 8 + 2 + 9 = 19
        # res[1][0] = 4*7 + 5*9 + 6*2 = 28 + 45 + 12 = 85
        # res[1][1] = 4*8 + 5*1 + 6*3 = 32 + 5 + 18 = 55
        res = self.mod.matrix_multiplication(a, b)
        self.assertEqual(res, [[31.0, 19.0], [85.0, 55.0]])

    def test_multiplication_incompatible_dimensions(self):
        a = [[1, 2], [3, 4]]
        b = [[1, 2, 3]]
        with self.assertRaises(ValueError):
            self.mod.matrix_multiplication(a, b)

    # --- 3. matrix_transpose ---
    def test_transpose_rectangular(self):
        a = [[1, 2, 3], [4, 5, 6]]
        expected = [[1, 4], [2, 5], [3, 6]]
        self.assertEqual(self.mod.matrix_transpose(a), expected)

    def test_transpose_invalid(self):
        with self.assertRaises(ValueError):
            self.mod.matrix_transpose([])
        with self.assertRaises(ValueError):
            self.mod.matrix_transpose([[1, 2], [3]])

    # --- 4. matrix_determinant ---
    def test_determinant_1x1_and_2x2(self):
        self.assertEqual(self.mod.matrix_determinant([[7]]), 7.0)
        self.assertEqual(self.mod.matrix_determinant([[1, 2], [3, 4]]), -2.0)

    def test_determinant_3x3(self):
        # det([[1, 2, 3], [0, 4, 5], [1, 0, 6]]) = 1*(24-0) - 2*(0-5) + 3*(0-4) = 24 + 10 - 12 = 22
        m = [[1, 2, 3], [0, 4, 5], [1, 0, 6]]
        self.assertEqual(self.mod.matrix_determinant(m), 22.0)

    def test_determinant_non_square(self):
        with self.assertRaises(ValueError):
            self.mod.matrix_determinant([[1, 2, 3], [4, 5, 6]])

    # --- 5. vector_dot_product ---
    def test_dot_product_valid(self):
        u = [1, 2, 3]
        v = [4, 5, 6]
        # 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
        self.assertEqual(self.mod.vector_dot_product(u, v), 32.0)

    def test_dot_product_orthogonal(self):
        u = [1, 0]
        v = [0, 1]
        self.assertEqual(self.mod.vector_dot_product(u, v), 0.0)

    def test_dot_product_mismatch_or_empty(self):
        with self.assertRaises(ValueError):
            self.mod.vector_dot_product([1, 2], [1, 2, 3])
        with self.assertRaises(ValueError):
            self.mod.vector_dot_product([], [])
        with self.assertRaises(TypeError):
            self.mod.vector_dot_product("123", [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
