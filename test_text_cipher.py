import unittest
import text_cipher


class TestTextCipher(unittest.TestCase):

    def setUp(self):
        self.mod = text_cipher

    # --- 1. caesar_cipher ---
    def test_caesar_encrypt_standard(self):
        res = self.mod.caesar_cipher("Hello, World!", 3, decrypt=False)
        self.assertEqual(res, "Khoor, Zruog!")

    def test_caesar_decrypt_standard(self):
        res = self.mod.caesar_cipher("Khoor, Zruog!", 3, decrypt=True)
        self.assertEqual(res, "Hello, World!")

    def test_caesar_large_shift(self):
        enc = self.mod.caesar_cipher("abc", 29, decrypt=False)
        self.assertEqual(enc, "def")
        dec = self.mod.caesar_cipher("def", 29, decrypt=True)
        self.assertEqual(dec, "abc")

    def test_caesar_invalid_input(self):
        with self.assertRaises(TypeError):
            self.mod.caesar_cipher(12345, 3)
        with self.assertRaises(TypeError):
            self.mod.caesar_cipher("test", "3")

    # --- 2. atbash_cipher ---
    def test_atbash_basic(self):
        # A <-> Z, B <-> Y, C <-> X
        res = self.mod.atbash_cipher("ABC xyz 123!")
        self.assertEqual(res, "ZYX cba 123!")

    def test_atbash_symmetry(self):
        # Атбаш самообратим: M == Atbash(Atbash(M))
        msg = "The Quick Brown Fox Jumps Over 13 Lazy Dogs."
        enc = self.mod.atbash_cipher(msg)
        self.assertNotEqual(enc, msg)
        self.assertEqual(self.mod.atbash_cipher(enc), msg)

    def test_atbash_invalid_input(self):
        with self.assertRaises(TypeError):
            self.mod.atbash_cipher(None)

    # --- 3. xor_cipher ---
    def test_xor_symmetry(self):
        msg = "Secret Data 2026!"
        key = "CryptoKey"
        encrypted = self.mod.xor_cipher(msg, key)
        self.assertNotEqual(encrypted, msg)
        decrypted = self.mod.xor_cipher(encrypted, key)
        self.assertEqual(decrypted, msg)

    def test_xor_empty_key(self):
        with self.assertRaises(ValueError):
            self.mod.xor_cipher("test", "")

    def test_xor_invalid_type(self):
        with self.assertRaises(TypeError):
            self.mod.xor_cipher(None, "key")

    # --- 4. vigenere_cipher ---
    def test_vigenere_encrypt(self):
        # Пример: ATTACKATDAWN с ключом LEMON -> LXFOPVEFRNHR
        res = self.mod.vigenere_cipher("ATTACKATDAWN", "LEMON", decrypt=False)
        self.assertEqual(res, "LXFOPVEFRNHR")

    def test_vigenere_decrypt(self):
        res = self.mod.vigenere_cipher("LXFOPVEFRNHR", "LEMON", decrypt=True)
        self.assertEqual(res, "ATTACKATDAWN")

    def test_vigenere_mixed_case_and_symbols(self):
        msg = "Attack at Dawn! 123"
        key = "lemon"
        enc = self.mod.vigenere_cipher(msg, key, decrypt=False)
        self.assertEqual(enc, "Lxfopv ef Rnhr! 123")
        dec = self.mod.vigenere_cipher(enc, key, decrypt=True)
        self.assertEqual(dec, msg)

    def test_vigenere_invalid_key_or_type(self):
        with self.assertRaises(ValueError):
            self.mod.vigenere_cipher("hello", "123!@#")
        with self.assertRaises(TypeError):
            self.mod.vigenere_cipher(100, "key")

    # --- 5. rail_fence_cipher ---
    def test_rail_fence_encrypt(self):
        # 3 рельса: "DEFENDTHEEASTWALL" -> "DNETLEEDHESWLFTAA"
        res = self.mod.rail_fence_cipher("DEFENDTHEEASTWALL", 3, decrypt=False)
        self.assertEqual(res, "DNETLEEDHESWLFTAA")

    def test_rail_fence_decrypt(self):
        res = self.mod.rail_fence_cipher("DNETLEEDHESWLFTAA", 3, decrypt=True)
        self.assertEqual(res, "DEFENDTHEEASTWALL")

    def test_rail_fence_boundary_and_exceptions(self):
        # rails <= 1 -> ValueError
        with self.assertRaises(ValueError):
            self.mod.rail_fence_cipher("test", 1)
        # rails >= len(text) -> возвращает без изменений
        self.assertEqual(self.mod.rail_fence_cipher("abc", 5), "abc")
        self.assertEqual(self.mod.rail_fence_cipher("", 3), "")

    def test_rail_fence_invalid_type(self):
        with self.assertRaises(TypeError):
            self.mod.rail_fence_cipher(1234, 3)
        with self.assertRaises(TypeError):
            self.mod.rail_fence_cipher("test", "3")


if __name__ == "__main__":
    unittest.main()
