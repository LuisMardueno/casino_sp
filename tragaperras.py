import pygame
import random
import os

# Inicializar Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Dimensiones de la ventana
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Máquina Tragamonedas")

# Fuentes
pygame.font.init()
font = pygame.font.SysFont(None, 36)

# Ruta de la carpeta de imágenes
image_folder = 'images'

# Cargar imágenes desde la carpeta "images"
clover_img = pygame.image.load(os.path.join(image_folder, 'clover.png'))  # 🍀
diamond_img = pygame.image.load(os.path.join(image_folder, 'diamond.png'))  # 💎
star_img = pygame.image.load(os.path.join(image_folder, 'star.png'))  # ⭐
cherry_img = pygame.image.load(os.path.join(image_folder, 'cherry.png'))  # 🍒

# Redimensionar imágenes para que se ajusten a la interfaz
clover_img = pygame.transform.scale(clover_img, (50, 50))
diamond_img = pygame.transform.scale(diamond_img, (50, 50))
star_img = pygame.transform.scale(star_img, (50, 50))
cherry_img = pygame.transform.scale(cherry_img, (50, 50))

# Diccionario de imágenes
symbol_images = {
    "🍀": clover_img,
    "💎": diamond_img,
    "⭐": star_img,
    "🍒": cherry_img
}

# Constantes
ROWS = 3
COLS = 3

symbol_count = {
    "🍀": 2,
    "💎": 4,
    "⭐": 6,
    "🍒": 8
}

symbol_value = {
    "🍀": 5,
    "💎": 4,
    "⭐": 3,
    "🍒": 2
}

# Funciones
def check_win(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def draw_text(text, x, y, color=WHITE):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def draw_slot_machine(columns):
    y_offset = 100
    for row in range(len(columns[0])):
        x_offset = 150
        for col in columns:
            symbol = col[row]
            image = symbol_images[symbol]  # Obtener la imagen del símbolo
            screen.blit(image, (x_offset, y_offset))
            x_offset += 100  # Espaciado entre columnas
        y_offset += 100  # Espaciado entre filas

def draw_button(x, y, width, height, text, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    draw_text(text, x + (width // 4), y + (height // 4))

def main():
    spin_result = None
    result_text = ""

    def spin_machine():
        nonlocal spin_result, result_text
        lines = 3  # Apuesta fija en 3 líneas
        bet = 10  # Apuesta fija de 10 por línea
        spin_result = get_slot_machine_spin(ROWS, COLS, symbol_count)
        winnings, winning_lines = check_win(spin_result, lines, bet, symbol_value)
        if winnings > 0:
            result_text = f"Ganaste en las líneas {', '.join(map(str, winning_lines))}!"
        else:
            result_text = "Perdiste, puñetas"

    running = True
    while running:
        screen.fill(BLACK)

        # Dibujar resultados
        if spin_result:
            draw_slot_machine(spin_result)
        draw_text(result_text, 50, 300)

        # Dibujar botón
        draw_button(250, 350, 100, 50, "Girar", GRAY, DARK_GRAY, spin_machine)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
