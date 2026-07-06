# Knight Energy

Juego de tablero 8×8 para el **Proyecto 2 — Inteligencia Artificial** (Universidad del Valle). Dos caballos compiten por recoger monedas (estrellas) en un tablero con casillas de energía (rayos). La **máquina** (caballo blanco) usa **minimax con poda alfa-beta**; el **humano** (caballo negro) juega con clic.

---

## Descripción

Cada jugador controla un caballo que se mueve en **L** (como en ajedrez). Cada movimiento cuesta **1 de energía**. Al caer en una casilla especial:

- **Moneda (estrella):** suma puntos al marcador.
- **Rayo:** recupera energía.

Si al **iniciar** tu turno no tienes energía suficiente para mover, pierdes **3 puntos** y se salta tu turno. La partida termina cuando no quedan monedas, cuando ambos jugadores se quedan sin energía, o cuando ninguno puede mover. Gana quien tenga **más puntos**.

---

## Controles

| Acción | Control |
|--------|---------|
| Elegir casilla válida | Clic en casilla **verde** |
| Menú: nombre | Escribir y Enter |
| Elegir dificultad | Clic en Principiante / Amateur / Experto |
| Salir | Cerrar ventana |

---

## Instalación

Requisitos: **Python 3.10+** (probado con 3.14 usando `pygame-ce`).

```bash
git clone https://github.com/ycvictoria/knight_energy_game.git
cd knight_energy_game/knight_energy
pip install -r requirements.txt
```

---

## Ejecución

```bash
cd knight_energy
python main.py
```

---

## Reglas del juego

| Concepto | Valor |
|----------|-------|
| Energía inicial | 7 |
| Costo por movimiento | 1 energía |
| Penalización (sin poder mover al inicio del turno) | −3 puntos |
| Monedas en tablero | 7 (valores: 2, 3, 4, 5, 6, 8, 9) |
| Rayos en tablero | 4 (valores: 2, 3, 4, 5) |
| Quién empieza | Máquina (caballo blanco) |

**Fin de partida:**

1. No quedan monedas en el tablero.
2. Ambos jugadores tienen **0 energía**.
3. Ningún jugador puede realizar un movimiento legal.

---
## Dificultad (profundidad minimax)

| Nivel | Profundidad | Descripción |
|-------|-------------|-------------|
| Principiante | 2 | Decisiones más simples |
| Amateur | 4 | Equilibrio razonable |
| Experto | 6 | Más anticipación táctica |

---

## Inteligencia artificial

- **Algoritmo:** minimax con **poda alfa-beta** y decisiones imperfectas (profundidad limitada).
- **MAX** = máquina (blanco); **MIN** = humano (negro).
- **Heurística** (nodos de corte):

  ```
  EVAL(s) = 1000·Δpuntos + 15·Δenergía + 5·Δmovilidad + 50·estrellas_restantes
  ```

- En estados terminales: **+∞** si gana MAX, **−∞** si gana MIN, **0** en empate.

---

## Estructura del proyecto

```
knight_energy_game/
├── knight_energy/
│   ├── main.py                  # Punto de entrada
│   ├── requirements.txt
│   └── src/
│       ├── config.py            # Constantes y dificultades
│       ├── models/state.py      # Estado del juego
│       ├── game_logic/engine.py # Reglas y movimientos
│       ├── ai/
│       │   ├── minimax.py       # Minimax + alfa-beta
│       │   └── heuristics.py    # Función de evaluación
│       └── ui/
│           ├── menu.py          # Menú inicial
│           ├── renderer.py      # Tablero y panel lateral
│           ├── animation.py     # Salto del caballo
│           ├── effects.py       # Iconos (moneda, rayo, barras)
│           └── feedback.py      # Mensajes de eventos

```

---

## Interfaz

- Tablero 8×8 con caballos Unicode (♘ / ♞).
- Panel lateral con **Points** (círculo dorado) y **Energy** (barra).
- Log de **Eventos** con explicación de cada jugada.
- Animación de salto en arco y feedback visual (+puntos, ±energía).

---

## Autor

Proyecto académico — Inteligencia Artificial, Universidad del Valle.

---

## Licencia

Uso académico según indicaciones del curso.
