# Constantes globales del juego Knight Energy (Proyecto 2 - IA)

# Dimensiones de la ventana y del tablero
WIDTH, HEIGHT = 800, 600
BOARD_SIZE = 8
# Tamaño de cada casilla en píxeles (tablero cuadrado sobre el alto de la ventana)
CELL_SIZE = HEIGHT // BOARD_SIZE
# Ancho del tablero en píxeles (el resto de WIDTH quedará para el panel en pasos posteriores)
BOARD_PIXELS = CELL_SIZE * BOARD_SIZE

# Colores RGB para el tablero y la interfaz
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_CELL = (240, 217, 181)
DARK_CELL = (181, 136, 99)
HIGHLIGHT_COLOR = (130, 151, 105)
PANEL_BG = (40, 44, 52)
# Variante más clara del panel, usada en menú y pantallas auxiliares
MENU_BG = (62, 68, 80)
TEXT_COLOR = (255, 255, 255)

# Reglas del juego según el enunciado
INITIAL_ENERGY = 7
PENALTY_POINTS = 3

# Valores fijos de casillas especiales (cada valor aparece exactamente una vez)
STAR_VALUES = [2, 3, 4, 5, 6, 8, 9]
ENERGY_VALUES = [2, 3, 4, 5]

# Identificadores de jugador en la lógica minimax (pasos posteriores)
MAX = "MAX"  # Máquina (caballo blanco)
MIN = "MIN"  # Humano (caballo negro)

# Profundidades del árbol minimax por nivel de dificultad
DIFFICULTIES = {
    "principiante": 2,
    "amateur": 4,
    "experto": 6,
}
