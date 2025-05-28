import random

def adivina(intentos_permitidos):
    numero_secreto = random.randint(0, 100)
    print("¡Bienvenido al juego de adivinar el número secreto!")
    print(f"Tenés {intentos_permitidos} intentos para adivinar un número entre 0 y 100.")

    for intento in range(1, intentos_permitidos + 1):
        try:
            adivinanza = int(input(f"Intento {intento}: Ingresá tu número: "))
        except ValueError:
            print("Eso no es un número válido. Intentá de nuevo.")
            continue

        if adivinanza < 0 or adivinanza > 100:
            print("El número debe estar entre 0 y 100.")
            continue

        if adivinanza == numero_secreto:
            print(f"¡Felicitaciones! Adivinaste el número en {intento} intentos.")
            return
        elif adivinanza < numero_secreto:
            print("Demasiado bajo.")
        else:
            print("Demasiado alto.")

    print(f"Se acabaron los intentos. El número secreto era {numero_secreto}.")

# Programa principal
if str(name) == "main":
    intentos = 5  # o podrías pedir al usuario que lo ingrese
    adivina(intentos)
