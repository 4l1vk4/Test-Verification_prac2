from typing import List

def caesar_cipher(text: str, shift: int, decrypt: bool = False) -> str:
    if not isinstance(text, str):
        raise TypeError("Текст должен быть строкой.")
    if not isinstance(shift, int):
        raise TypeError("Сдвиг должен быть целым числом.")
    
    effective_shift = (-shift) % 26 if decrypt else shift % 26
    res: List[str] = []
    for char in text:
        if 'a' <= char <= 'z':
            res.append(chr(ord('a') + (ord(char) - ord('a') + effective_shift) % 26))
        elif 'A' <= char <= 'Z':
            res.append(chr(ord('A') + (ord(char) - ord('A') + effective_shift) % 26))
        else:
            res.append(char)
    return "".join(res)


def atbash_cipher(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Текст должен быть строкой.")
    
    res: List[str] = []
    for char in text:
        if 'a' <= char <= 'z':
            res.append(chr(ord('z') - (ord(char) - ord('a'))))
        elif 'A' <= char <= 'Z':
            res.append(chr(ord('Z') - (ord(char) - ord('A'))))
        else:
            res.append(char)
    return "".join(res)


def xor_cipher(text: str, key: str) -> str:
    if not isinstance(text, str) or not isinstance(key, str):
        raise TypeError("Текст и ключ должны быть строками.")
    if len(key) == 0:
        raise ValueError("Ключ шифрования не может быть пустым.")
    
    res: List[str] = []
    key_len = len(key)
    for i, char in enumerate(text):
        k_char = key[i % key_len]
        res.append(chr(ord(char) ^ ord(k_char)))
    return "".join(res)


def vigenere_cipher(text: str, key: str, decrypt: bool = False) -> str:
    if not isinstance(text, str) or not isinstance(key, str):
        raise TypeError("Текст и ключ должны быть строками.")
    
    clean_key = [c.lower() for c in key if c.isalpha()]
    if not clean_key:
        raise ValueError("Ключ Виженера должен содержать хотя бы одну букву латинского алфавита.")
    
    res: List[str] = []
    k_idx = 0
    key_len = len(clean_key)
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            base = ord('A') if is_upper else ord('a')
            k_shift = ord(clean_key[k_idx % key_len]) - ord('a')
            shift = (-k_shift) % 26 if decrypt else k_shift % 26
            res.append(chr(base + (ord(char) - base + shift) % 26))
            k_idx += 1
        else:
            res.append(char)
    return "".join(res)


def rail_fence_cipher(text: str, rails: int, decrypt: bool = False) -> str:
    if not isinstance(text, str):
        raise TypeError("Текст должен быть строкой.")
    if not isinstance(rails, int):
        raise TypeError("Число рельсов должно быть целым числом.")
    if rails <= 1:
        raise ValueError("Число рельсов должно быть строго больше 1.")
    
    if len(text) <= 1 or rails >= len(text):
        return text
    
    if not decrypt:
        fence: List[List[str]] = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        for char in text:
            fence[rail].append(char)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        return "".join("".join(row) for row in fence)
    else:
        n = len(text)
        pattern = [[False] * n for _ in range(rails)]
        rail = 0
        direction = 1
        for col in range(n):
            pattern[rail][col] = True
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        
        idx = 0
        grid = [[''] * n for _ in range(rails)]
        for r in range(rails):
            for c in range(n):
                if pattern[r][c] and idx < n:
                    grid[r][c] = text[idx]
                    idx += 1
        
        result: List[str] = []
        rail = 0
        direction = 1
        for col in range(n):
            result.append(grid[rail][col])
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction
        return "".join(result)
