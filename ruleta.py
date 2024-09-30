import random

# Definimos los colores de la ruleta
rojos = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
negros = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

# Simula el giro de la ruleta (del 0 al 36)
def spin_roulette():
    return random.randint(0, 36)

# Función para determinar si el número es rojo, negro o verde
def get_color(number):
    if number == 0:
        return "verde"
    elif number in rojos:
        return "rojo"
    elif number in negros:
        return "negro"
    return None

# Función para jugar
def play_roulette(bet_type, bet_value):
    # Girar la ruleta
    result = spin_roulette()
    color = get_color(result)

    print(f"El número es {result} ({color}).")

    # Comprobamos qué tipo de apuesta es
    if bet_type == "número":
        # Apuesta a número exacto
        if result == bet_value:
            return "¡Has ganado la apuesta al número exacto! Paga 35:1"
        else:
            return "Lo siento, no has acertado el número."

    elif bet_type == "color":
        # Apuesta a color (rojo o negro)
        if bet_value == color:
            return f"¡Has ganado la apuesta al color {color}! Paga 1:1"
        else:
            return f"Lo siento, el color fue {color}."

    elif bet_type == "paridad":
        # Apuesta a par o impar
        if result == 0:
            return "Lo siento, cayó el 0."
        if (bet_value == "par" and result % 2 == 0) or (bet_value == "impar" and result % 2 != 0):
            return f"¡Has ganado la apuesta a {bet_value}! Paga 1:1"
        else:
            return f"Lo siento, el número fue {result}."

    return "Tipo de apuesta no válido."

# Ejemplo de cómo jugar
def main():
    print("Bienvenido a la ruleta.")
    
    while True:
        print("\nOpciones de apuesta:")
        print("1. Apostar a un número exacto")
        print("2. Apostar a un color (rojo o negro)")
        print("3. Apostar a par o impar")
        print("4. Salir")

        opcion = input("\nElige tu tipo de apuesta: ")
        
        if opcion == "1":
            # Apuesta a un número exacto
            numero = int(input("¿A qué número (0-36) quieres apostar? "))
            if 0 <= numero <= 36:
                resultado = play_roulette("número", numero)
            else:
                print("Número no válido.")
                continue

        elif opcion == "2":
            # Apuesta a color
            color = input("¿A qué color quieres apostar? (rojo/negro): ").lower()
            if color in ["rojo", "negro"]:
                resultado = play_roulette("color", color)
            else:
                print("Color no válido.")
                continue

        elif opcion == "3":
            # Apuesta a par o impar
            paridad = input("¿A qué quieres apostar? (par/impar): ").lower()
            if paridad in ["par", "impar"]:
                resultado = play_roulette("paridad", paridad)
            else:
                print("Opción no válida.")
                continue

        elif opcion == "4":
            print("Gracias por jugar. ¡Hasta la próxima!")
            break
        else:
            print("Opción no válida.")
            continue

        # Mostrar resultado de la apuesta
        print(resultado)

if __name__ == "__main__":
    main()
