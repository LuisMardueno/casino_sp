import pygame
import random
import time

# Inicializa Pygame
pygame.init()

# Colores
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Blackjack con Botones')

# Inicializar reloj
clock = pygame.time.Clock()

# Definir el mazo
SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 10, 'queen': 10, 'king': 10, 'ace': 11}

# Variables globales del juego
deck = []
player_hand = []
dealer_hand = []
player_turn = True
game_over = False
player_busted = False
dealer_busted = False
player_wins = False
hit_pause = False  # Variable para manejar la pausa

# Cargar las imágenes de las cartas y redimensionarlas
def load_card_images():
    images = {}
    for suit in SUITS:
        for rank in RANKS:
            image_path = f'images/{rank}_of_{suit}.png'
            card_image = pygame.image.load(image_path).convert_alpha()
            card_image = pygame.transform.scale(card_image, (int(card_image.get_width() * 0.125), int(card_image.get_height() * 0.125)))
            images[(rank, suit)] = card_image
    back_image = pygame.image.load('images/back.png').convert_alpha()
    back_image = pygame.transform.scale(back_image, (int(back_image.get_width() * 0.125), int(back_image.get_height() * 0.125)))
    images['back'] = back_image
    return images

# Función para crear un mazo de cartas
def create_deck():
    deck = []
    for suit in SUITS:
        for rank in RANKS:
            deck.append((rank, suit))
    random.shuffle(deck)
    return deck

# Función para calcular el valor de una mano
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        rank = card[0]
        value += VALUES[rank]
        if rank == 'ace':
            aces += 1
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Función para mostrar la mano de cartas con imágenes
def display_hand(hand, pos, images, hide_second=False):
    x_offset = 0
    for i, card in enumerate(hand):
        if i == 1 and hide_second:
            screen.blit(images['back'], (pos[0] + x_offset, pos[1]))
        else:
            screen.blit(images[card], (pos[0] + x_offset, pos[1]))
        x_offset += 40  # Espaciado entre cartas

# Función para dibujar botones
def draw_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action:
            return action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    
    small_text = pygame.font.SysFont("poppy", 20)
    text_surface = small_text.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=((x + (width / 2)), (y + (height / 2))))
    screen.blit(text_surface, text_rect)

# Función para mostrar texto en la pantalla
def display_text(text, x, y, size=30, color=BLACK):
    font = pygame.font.SysFont("poppyms", size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Juego principal
def main():
    global deck, player_hand, dealer_hand, player_turn, game_over, player_busted, dealer_busted, player_wins, hit_pause
    # Cargar imágenes de las cartas
    card_images = load_card_images()

    def start_game():
        global deck, player_hand, dealer_hand, player_turn, game_over, player_busted, dealer_busted, player_wins, hit_pause
        deck = create_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        player_turn = True
        game_over = False
        player_busted = False
        dealer_busted = False
        player_wins = False
        hit_pause = False

    def hit():
        global player_turn, game_over, player_busted, hit_pause
        if player_turn and not game_over and not hit_pause:
            player_hand.append(deck.pop())
            hit_pause = True  # Pausar la acción de pedir carta
            if calculate_hand_value(player_hand) > 21:
                player_busted = True
                player_turn = False
                game_over = True
            # Esperar un poco para la próxima carta
            pygame.time.set_timer(pygame.USEREVENT, 500)  # 500 milisegundos de pausa

    def stand():
        global player_turn, game_over, player_wins, dealer_busted
        if player_turn and not game_over:
            player_turn = False
            while calculate_hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
            if calculate_hand_value(dealer_hand) > 21:
                dealer_busted = True
                game_over = True
            game_over = True
            player_wins = calculate_hand_value(player_hand) > calculate_hand_value(dealer_hand)

    # Iniciar el juego
    start_game()

    while True:
        screen.fill(GREEN)

        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)

        # Mostrar las manos
        display_hand(player_hand, (50, 100), card_images)  # Mano del jugador
        display_hand(dealer_hand, (50, 300), card_images, hide_second=player_turn)  # Mano del crupier

        # Mostrar los valores de las manos
        display_text(f"Mano del jugador: {player_value}", 50, 70)
        if not player_turn:
            display_text(f"Mano del crupier: {dealer_value}", 50, 270)
        else:
            display_text("Mano del crupier: ?", 50, 270)

        # Dibujar botones
        if not hit_pause:
            draw_button("Pedir carta", 600, 100, 150, 50, WHITE, (200, 200, 200), hit)
        draw_button("Plantarse", 600, 200, 150, 50, WHITE, (200, 200, 200), stand)
        if game_over:
            draw_button("Nuevo juego", 600, 300, 150, 50, WHITE, (200, 200, 200), start_game)

        # Verificar si alguien ha ganado y mostrar el resultado
        if game_over:
            if player_busted:
                display_text("El jugador pierde (Bust)", 300, 400, size=40, color=(255, 0, 0))
            elif dealer_busted:
                display_text("El crupier pierde (Bust)", 300, 400, size=40, color=(0, 255, 0))
            elif player_wins:
                display_text("El jugador gana", 300, 400, size=40, color=(0, 255, 0))
            else:
                display_text("El crupier gana", 300, 400, size=40, color=(255, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.USEREVENT:
                hit_pause = False  # Desactivar la pausa una vez que haya pasado el tiempo
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Detener el temporizador

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
