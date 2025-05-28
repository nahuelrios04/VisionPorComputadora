import random 
import msvcrt 
def adivinar(max_trys):
    secretNumber = random.randit(0,100)
    trys=0
print("Bienvenido al sistema. Iniciando juego de adivinar un numero")
print("Tienes {max_trys} para adivinar un numero comprendido entre 0 y 100")

while trys<max_trys:

