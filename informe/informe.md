# Informe — Proyecto 2: Knight Energy

**Curso:** Inteligencia Artificial — Universidad del Valle  
**Juego:** Knight Energy (humano vs máquina, minimax con decisiones imperfectas)

---

## 1. Definición formal del juego

| Elemento | Descripción |
|----------|-------------|
| **Estado inicial** | Tablero 8×8; posiciones aleatorias de 2 caballos, 7 estrellas (2,3,4,5,6,8,9) y 4 rayos (2,3,4,5); energía inicial 7; turno MAX (máquina/blanco). |
| **Operadores** | Mover caballo en L a casilla vacía o con ítem; costo 1 energía; recoger estrella suma puntos; rayo suma energía; casilla consumida. |
| **Prueba terminal** | Sin estrellas en tablero, o ningún jugador puede mover legalmente. |
| **Utilidad terminal** | Comparación de puntajes: gana quien tenga más; empate si iguales. |

---

## 2. Función heurística

En nodos de corte (profundidad límite) se usa una **combinación lineal** desde la perspectiva de **MAX** (máquina):

```
EVAL(s) = w1·f1(s) + w2·f2(s) + w3·f3(s) + w4·f4(s)
```

| Feature | Definición | Peso | Justificación |
|---------|------------|------|---------------|
| **f1** | `white_score - black_score` | 1000 | Objetivo principal del juego. |
| **f2** | `white_energy - black_energy` | 15 | Más energía permite más movimientos y evita penalizaciones. |
| **f3** | movilidad MAX − movilidad MIN | 5 | Más opciones tácticas para la máquina. |
| **f4** | suma de valores de estrellas restantes | 50 | Aproxima botín aún disponible en el tablero. |

En estados **terminales**:
- MAX gana → `+∞`
- MIN gana → `−∞`
- Empate → `0`

Implementación: `knight_energy/src/ai/heuristics.py`

---

## 3. Minimax y poda alfa-beta

- **MAX** = máquina (caballo blanco); **MIN** = humano (caballo negro).
- Profundidad límite según dificultad: principiante 2, amateur 4, experto 6 (plies).
- En nodos sin movimientos legales se modela la **penalización** (−3 pts, pierde turno).
- **Poda alfa-beta** reduce nodos explorados sin cambiar la decisión minimax.

Implementación: `knight_energy/src/ai/minimax.py`

---

## 4. Comportamiento observado

### Casos donde la IA juega bien
- Prioriza estrellas de alto valor cuando están a 1–2 movimientos dentro del horizonte.
- En nivel experto (profundidad 6) evita quedarse sin energía antes de rayos cercanos.
- Aprovecha penalizaciones del rival cuando el árbol las anticipa.

### Casos donde falla o no es óptima
- **Efecto horizonte:** captura una estrella pequeña y deja una grande al rival fuera del límite de profundidad.
- **Profundidad 2 (principiante):** decisiones claramente miope; esperado en decisiones imperfectas.
- **f4 global:** no distingue qué estrellas son alcanzables antes que el rival.
- MIN se asume **óptimo** en el árbol; un humano irregular puede hacer que la máquina “anticipe mal”.

---

## 5. Limitaciones y trabajo futuro

- Ordenamiento de movimientos para mejorar poda.
- Búsqueda quiescente en capturas de estrellas.
- Calibración experimental de pesos w1…w4.

---

## 6. Ejecución

```bash
cd knight_energy
pip install -r requirements.txt
python main.py
```
