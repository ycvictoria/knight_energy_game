import copy
import random

from src.config import BOARD_SIZE, ENERGY_VALUES, INITIAL_ENERGY, MAX, STAR_VALUES
from src.game_logic.engine import is_game_over


class GameState:
    """
    Representa un estado completo del juego: tablero, caballos, puntajes y turno.

    Convención de coordenadas: (fila, columna) con origen en la esquina superior izquierda.
    MAX (máquina) usa el caballo blanco; MIN (humano) usa el caballo negro.
    """

    def __init__(self, generate_random=False):
        # Matriz 8x8: None o dict con 'type' ('star'|'lightning') y 'value'
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        # Posiciones iniciales por defecto (se reemplazan si generate_random=True)
        self.white_pos = (0, 0)
        self.black_pos = (7, 7)

        self.white_energy = INITIAL_ENERGY
        self.black_energy = INITIAL_ENERGY
        self.white_score = 0
        self.black_score = 0

        # La máquina (MAX) siempre inicia según el enunciado
        self.turn = MAX

        # Contador de estrellas restantes (optimiza la condición de fin de juego)
        self.stars_count = 0

        if generate_random:
            self._initialize_random_board()

    def _initialize_random_board(self):
        """
        Coloca caballos, estrellas y rayos en posiciones aleatorias sin repetir casilla.
        Cumple la regla del PDF: posiciones iniciales no pueden coincidir.
        """
        all_positions = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
        random.shuffle(all_positions)

        self.white_pos = all_positions.pop()
        self.black_pos = all_positions.pop()

        for value in STAR_VALUES:
            row, col = all_positions.pop()
            self.board[row][col] = {"type": "star", "value": value}
            self.stars_count += 1

        for value in ENERGY_VALUES:
            row, col = all_positions.pop()
            self.board[row][col] = {"type": "lightning", "value": value}

    def is_terminal(self):
        """
        Prueba terminal del juego: delega en is_game_over del motor de reglas.
        Usada por minimax para detectar hojas del árbol (pasos posteriores).
        """
        return is_game_over(self)

    def clone(self):
        """Copia profunda del estado (necesaria para el árbol minimax en pasos posteriores)."""
        return copy.deepcopy(self)
