import random
import sys
import termios
import tty

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def adivinar(Maxtrys):
    SecretNumber = random.randint(0, 100)
    trys = 0
    print("¡Bienvenido al juego de adivinar el número!")
    print(f"Tienes {Maxtrys} trys para adivinar un número entre 0 y 100.")
    
    while trys < Maxtrys:
        try:
            guess = int(input("Ingresa tu número: "))
            while 0 >guess or guess > 100:
                print("El numero ingresado esta fuera de rango. Ingrese nuevamente...")
                guess = int(input("Ingresa tu número: "))
            trys += 1
            
            if guess == SecretNumber:
                print(f"¡Felicidades! Adivinaste el número en {trys} intentos.")
                print("Presiona cualquier tecla para continuar...")
                getch() 
                return
            elif guess < SecretNumber:
                print("El número secreto es mayor.")
            else:
                print("El número secreto es menor.")
                
        except ValueError:
            print("Por favor, ingresa un número válido.")
    
    print(f"\n¡GAME OVER! Has superado el número máximo de trys ({Maxtrys}).")
    print(f"El número secreto era: {SecretNumber}.")
adivinar(int(input("Ingrese numero de intentos: ")))
