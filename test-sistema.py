from SistemaCesarYRsa import *


def probar(nombre, condicion):
    print(("OK    " if condicion else "FALLO ") + nombre)
    return condicion


def lanza_error(funcion, *args):
    try:
        funcion(*args)
        return False
    except ValueError:
        return True


publica, privada = generar_claves(61, 53, 17)
pub_chica, priv_chica = generar_claves(3, 11, 3)
mensaje_rsa = "Hola mundo"

resultados = [
    probar("Cesar cifra con k=3", cifrar_cesar("Hola Mundo, XYZ!", 3) == "Krod Pxqgr, ABC!"),
    probar("Cesar descifra con k=3", descifrar_cesar("Krod Pxqgr, ABC!", 3) == "Hola Mundo, XYZ!"),
    probar("Cesar k=0 no cambia el texto", cifrar_cesar("Hola", 0) == "Hola"),
    probar("Cesar k=26 da la vuelta completa", cifrar_cesar("Hola", 26) == "Hola"),
    probar("Fuerza bruta incluye el original", (3, "Hola Mundo") in fuerza_bruta_cesar("Krod Pxqgr")),
    probar("Fuerza bruta devuelve 26 opciones", len(fuerza_bruta_cesar("abc")) == 26),
    probar("es_primo(61) es True", es_primo(61)),
    probar("es_primo(1) es False", not es_primo(1)),
    probar("es_primo(33) es False", not es_primo(33)),
    probar("mcd(20, 3) = 1", mcd(20, 3) == 1),
    probar("mcd(48, 18) = 6", mcd(48, 18) == 6),
    probar("inverso_modular(3, 20) = 7", inverso_modular(3, 20) == 7),
    probar("inverso_modular(17, 3120) = 2753", inverso_modular(17, 3120) == 2753),
    probar("potencia_modular(4, 3, 33) = 31", potencia_modular(4, 3, 33) == 31),
    probar("potencia_modular coincide con pow", potencia_modular(65, 17, 3233) == pow(65, 17, 3233)),
    probar("Claves con p=61, q=53, e=17", publica == (17, 3233) and privada == (2753, 3233)),
    probar("Claves con p=3, q=11, e=3", pub_chica == (3, 33) and priv_chica == (7, 33)),
    probar("Cifrar 65 da 2790", cifrar_numero(65, publica) == 2790),
    probar("Cifrar 4 con n=33 da 31", cifrar_numero(4, pub_chica) == 31),
    probar("Descifrar 31 con n=33 da 4", descifrar_numero(31, priv_chica) == 4),
    probar("RSA ida y vuelta de un texto", descifrar_rsa(cifrar_rsa(mensaje_rsa, publica), privada) == mensaje_rsa),
    probar("Error si p no es primo", lanza_error(generar_claves, 4, 11, 3)),
    probar("Error si p y q son iguales", lanza_error(generar_claves, 7, 7, 5)),
    probar("Error si e no es coprimo con phi", lanza_error(generar_claves, 3, 11, 4)),
    probar("Error si n es menor o igual a 255", lanza_error(cifrar_rsa, "hola", pub_chica)),
]

print(f"\n{sum(resultados)} de {len(resultados)} pruebas pasaron")