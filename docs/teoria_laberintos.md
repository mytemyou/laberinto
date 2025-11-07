# Teoría de la Resolución de Laberintos

Los laberintos representan problemas de **búsqueda en grafos**.  
Un camino óptimo se define como la secuencia de nodos que conecta el inicio `S` con la meta `G` minimizando el coste acumulado.

## Algoritmos Clásicos

| Algoritmo | Tipo de búsqueda | Garantiza óptimo | Requiere heurística |
|------------|------------------|------------------|----------------------|
| BFS | Uniforme (coste = 1) | ✅ | ❌ |
| Dijkstra | Costes variables | ✅ | ❌ |
| A* | Costes variables | ✅ | ✅ |
| DFS | Profundidad | ❌ | ❌ |

---

## Laberintos Condicionales

Cuando existen condiciones (llaves, puertas, interruptores), el estado deja de ser solo `(x, y)` y pasa a ser `(x, y, condiciones)`.  
El problema se transforma en **planificación en espacios de estado**.

Esto provoca un crecimiento exponencial del número de nodos y eleva la complejidad a **PSPACE-completa** o más, según las reglas.
