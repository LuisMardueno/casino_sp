import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO = 800
ALTO = 400

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Colores para el destello del texto
COLORES = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Carrera de Caballos")

# Velocidades aleatorias de los caballos
def obtener_velocidad():
    return random.randint(1, 5)

# Cargar imagen de fondo
fondo = pygame.image.load("estadio.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Ajustar el tamaño de la imagen de fondo

# Cargar imágenes de los caballos
caballo1 = pygame.image.load("flutter.png")
caballo2 = pygame.image.load("bojack.png")
caballo3 = pygame.image.load("epona.png")

# Cambiar el tamaño de las imágenes de los caballos (opcional)
caballo1 = pygame.transform.scale(caballo1, (100, 50))
caballo2 = pygame.transform.scale(caballo2, (100, 50))
caballo3 = pygame.transform.scale(caballo3, (100, 50))

# Posiciones iniciales de los caballos
posiciones = [130, 190, 280]
x1, x2, x3 = 0, 0, 0

# Reloj
reloj = pygame.time.Clock()

# Bucle principal del juego
ejecutando = True
ganador = None
contador_colores = 0  # Contador para alternar colores
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Dibujar la imagen de fondo
    pantalla.blit(fondo, (0, 0))  # Dibujar el fondo en la posición (0, 0)

    # Dibujar los caballos
    pantalla.blit(caballo1, (x1, posiciones[0]))
    pantalla.blit(caballo2, (x2, posiciones[1]))
    pantalla.blit(caballo3, (x3, posiciones[2]))

    # Movimiento de los caballos
    if not ganador:
        x1 += obtener_velocidad()
        x2 += obtener_velocidad()
        x3 += obtener_velocidad()

    # Comprobar si hay ganador
    if x1 >= ANCHO - caballo1.get_width() and not ganador:
        ganador = "Caballo 1"
    elif x2 >= ANCHO - caballo2.get_width() and not ganador:
        ganador = "Caballo 2"
    elif x3 >= ANCHO - caballo3.get_width() and not ganador:
        ganador = "Caballo 3"

    # Mostrar el ganador con destello de colores
    if ganador:
        fuente = pygame.font.Font(None, 74)
        
        # Alternar colores del mensaje
        color_actual = COLORES[contador_colores // 10 % len(COLORES)]  # Cambia de color cada 10 cuadros
        
        texto = fuente.render(f"¡{ganador} gana!", True, color_actual)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2 - texto.get_height()//2))
        
        # Incrementar el contador para cambiar de color
        contador_colores += 1

    # Actualizar pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    reloj.tick(60)

# Salir de Pygame
pygame.quit()
