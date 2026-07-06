"""
Función de utilidad heurística para minimax con decisiones imperfectas.

Paso 4: evaluación simple con diferencia de puntos y energía.
En el Paso 5 se ampliará con más features y poda alfa-beta.
"""


def eval_state(state):
    """
    Evalúa un estado no terminal desde la perspectiva de MAX (máquina).

    EVAL(s) = w1 * f1(s) + w2 * f2(s)
      f1: diferencia de puntajes (blanco - negro)
      f2: diferencia de energía (blanco - negro)
    """
    f1 = state.white_score - state.black_score
    f2 = state.white_energy - state.black_energy

    w1 = 1000
    w2 = 10

    return (w1 * f1) + (w2 * f2)


def utility(state):
    """
    Utilidad para nodos hoja del árbol minimax.
    En terminales retorna la diferencia real de puntos; si no, la heurística.
    """
    if state.is_terminal():
        score_diff = state.white_score - state.black_score
        if score_diff > 0:
            return 10_000 + score_diff
        if score_diff < 0:
            return -10_000 + score_diff
        return 0

    return eval_state(state)
