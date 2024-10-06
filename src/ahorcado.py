import random
import sys
from .recursos.ahorcado_recursos import HANGMANPICS, HANGMANPIC_SUCCESS, HANGMANPIC_DEATH, palabras_ahorcado
import pyfiglet
from colorama import Fore, Style, init
import os

### Apuntes
# Valorar si hay forma mejor deshacerme del uso de la copia lista por su método remove
#

class Ahorcado():
    def __init__(self) -> None:
        self.intentos = list()
        self.display_palabra_lista = list()
        self.dibujo = ""

    def welcome(self):
        init(autoreset=True)
        self.titulo = pyfiglet.figlet_format("HANGMAN", font="poison")
        print(Fore.LIGHTRED_EX + self.titulo)

    def jugar(self):
        self.seleccionar_dificultad()
        self.generar_palabra()
        self.pintar_dibujo()
        self.pintar_display()
        while "_" in self.display_palabra_lista and self.vidas_restantes > 0:
            self.introducir_letra()
            if "_" not in self.display_palabra_lista:
                self.actualizar_dibujo("win")
                print("\n¡Enhorabuena, has ganado!")
            elif self.vidas_restantes == 0:
                self.actualizar_dibujo("loss")
                print("\n¡NOOOO, has matado al ahorcado!")
                self.pintar_dibujo()
                print("\nHas perdido.")
                break
            else:
                self.actualizar_dibujo(self.vidas_restantes)

            self.actualizar_display()
            self.pintar_dibujo()
            self.pintar_display()

        self.reset()

    
    def seleccionar_dificultad(self,retry=False):
        if not retry:
            self.vidas_restantes = input("""\nElige tu dificultad introduciendo el número de vidas:                                
            Insecto: 6 vidas
            Principiante: 5 vidas
            Corriente: 4 vidas
            Atrevido: 3 vidas
            Leyenda: 2 vidas
            Puto colgao: 1 vida
            """)
        else:
            self.vidas_restantes = input("\n")
        try:
            self.vidas_restantes = int(self.vidas_restantes)
            if self.vidas_restantes < 1 or self.vidas_restantes > 6:
                raise IndexError("Valor fuera de rango.")
        except IndexError:
            print("El valor que has introducido está fuera del rango permitido. Inténtalo de nuevo.")
            self.seleccionar_dificultad(retry=True)
        except:
            print("El valor que has introducido no es correcto. Inténtalo de nuevo.")
            self.seleccionar_dificultad(retry=True)

        self.dibujo = HANGMANPICS[-self.vidas_restantes-1]


    def pintar_dibujo(self):
        """"""
        print(self.dibujo)

    def pintar_display(self):
        """"""
        display_palabra = "".join(self.display_palabra_lista)
        print(display_palabra)
        print(f"Te quedan {self.vidas_restantes} vidas restantes.")





    def generar_palabra(self) -> None:
        """"""
        self.palabra_turno_lista = list(random.choice(palabras_ahorcado).lower()) 
        self.display_palabra_lista = list("_"*len(self.palabra_turno_lista))



    def introducir_letra(self,retry=False) -> bool:
        """"""
        if not retry:
            self.letra_ultimo_intento = input("\n\nEscribe una letra:")
        else:
            self.letra_ultimo_intento = input("\n")
        try:
            if not self.letra_ultimo_intento.isalpha():
                raise ValueError("El valor introducido no es una letra.")
        except:
            print("No has introducido una letra válida. Inténtalo de nuevo.")
            self.introducir_letra(retry=True)
        if self.letra_ultimo_intento in self.palabra_turno_lista:
            print("¡Acierto!")
                
        else: 
            print("¡Error!")
            self.vidas_restantes -= 1
            resultado = "error"
            
            
    def actualizar_display(self):
        while self.letra_ultimo_intento in self.palabra_turno_lista:
            posicion_letra = self.palabra_turno_lista.index(self.letra_ultimo_intento)
            self.display_palabra_lista[posicion_letra] = self.letra_ultimo_intento.upper()
            self.palabra_turno_lista[posicion_letra] = "_"

    
    def actualizar_dibujo(self,resultado="error") -> None:
        """"""
        if resultado == "win":
            self.dibujo = HANGMANPIC_SUCCESS
        elif resultado == "loss":
            self.dibujo = HANGMANPIC_DEATH
        else:
            self.dibujo = HANGMANPICS[-self.vidas_restantes-1]

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def reset(self):
        seguir_jugando = input("\n¿Deseas volver a jugar? [Y/N]\n")
        if seguir_jugando.upper()[0] == "Y":
            self.__init__()
            self.jugar()
        else:
            print("\n¡Ha sido un placer!\n")