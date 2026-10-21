def desplazar_letra(letra: str, k: int) -> str:
    if not (letra.isascii() and letra.isalpha()):
        return letra
    base = ord('A') if letra.isupper() else ord('a')
    posicion = ord(letra) - base
    nueva = (posicion + k) % 26
    return chr(nueva + base)


def cifrar_cesar(texto: str, k: int) -> str:
    return "".join(map(lambda c: desplazar_letra(c, k), texto))


def descifrar_cesar(texto: str, k: int) -> str:
    return cifrar_cesar(texto, -k)


def fuerza_bruta_cesar(texto_cifrado: str) -> list:
    return [(k, descifrar_cesar(texto_cifrado, k)) for k in range(26)]


def es_primo(n: int) -> bool:
    return n > 1 and all(n % d != 0 for d in range(2, int(n ** 0.5) + 1))


def mcd(a: int, b: int) -> int:
    return a if b == 0 else mcd(b, a % b)


def euclides_extendido(a: int, b: int) -> tuple:
    if b == 0:
        return (a, 1, 0)
    g, x, y = euclides_extendido(b, a % b)
    return (g, y, x - (a // b) * y)


def inverso_modular(e: int, phi: int) -> int:
    g, x, _ = euclides_extendido(e, phi)
    if g != 1:
        raise ValueError("e y phi(n) no son coprimos: no existe inverso modular")
    return x % phi


def potencia_modular(base: int, exponente: int, modulo: int) -> int:
    if exponente == 0:
        return 1
    mitad = potencia_modular(base, exponente // 2, modulo)
    cuadrado = (mitad * mitad) % modulo
    return (cuadrado * base) % modulo if exponente % 2 == 1 else cuadrado


def generar_claves(p: int, q: int, e: int) -> tuple:
    if not (es_primo(p) and es_primo(q)) or p == q:
        raise ValueError("p y q deben ser primos distintos")
    n = p * q
    phi = (p - 1) * (q - 1)
    if not (1 < e < phi and mcd(e, phi) == 1):
        raise ValueError("e debe cumplir 1 < e < phi(n) y mcd(e, phi(n)) = 1")
    d = inverso_modular(e, phi)
    return ((e, n), (d, n))


def cifrar_numero(m: int, clave_publica: tuple) -> int:
    e, n = clave_publica
    return potencia_modular(m, e, n)


def descifrar_numero(c: int, clave_privada: tuple) -> int:
    d, n = clave_privada
    return potencia_modular(c, d, n)


def cifrar_rsa(texto: str, clave_publica: tuple) -> list:
    _, n = clave_publica
    if n <= 255:
        raise ValueError("n debe ser mayor que 255 (elige primos más grandes)")
    return list(map(lambda c: cifrar_numero(ord(c), clave_publica), texto))


def descifrar_rsa(cifrado: list, clave_privada: tuple) -> str:
    return "".join(map(lambda x: chr(descifrar_numero(x, clave_privada)), cifrado))


def demo_cesar() -> None:
    mensaje = input("Mensaje: ")
    k = int(input("Llave k (0-25): "))
    cifrado = cifrar_cesar(mensaje, k)
    print("Cifrado     :", cifrado)
    print("Descifrado  :", descifrar_cesar(cifrado, k))
    print("\nAtaque de fuerza bruta (las 26 posibilidades):")
    list(map(lambda par: print(f"  k={par[0]:2d} -> {par[1]}"), fuerza_bruta_cesar(cifrado)))


def demo_rsa() -> None:
    p = int(input("Primo p (ej. 61): "))
    q = int(input("Primo q (ej. 53): "))
    e = int(input("Exponente público e (ej. 17): "))
    publica, privada = generar_claves(p, q, e)
    print(f"n = {p*q}, phi(n) = {(p-1)*(q-1)}")
    print("Clave pública  (e, n):", publica)
    print("Clave privada  (d, n):", privada)
    mensaje = input("Mensaje: ")
    cifrado = cifrar_rsa(mensaje, publica)
    print("Cifrado     :", cifrado)
    print("Descifrado  :", descifrar_rsa(cifrado, privada))


def menu() -> None:
    print("1) Cifrado César\n2) RSA simplificado\n3) Salir")
    opcion = input("Opción: ")
    if opcion == "1":
        demo_cesar()
    elif opcion == "2":
        demo_rsa()
    else:
        return
    menu()


if __name__ == "__main__":
    menu()