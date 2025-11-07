# Algoritmos de Laberintos y Búsqueda en Espacios de Estado

Proyecto educativo sobre resolución de laberintos con algoritmos clásicos de búsqueda:
- **BFS** (anchura)
- **DFS** (profundidad)
- **Dijkstra** y **A***
- **Laberintos condicionales** (búsqueda con estados extendidos)

Incluye animación en consola y ejemplos explicativos.

## Estructura

| Carpeta | Contenido |
|----------|------------|
| `src/` | Código fuente de los algoritmos |
| `examples/` | Archivos de laberintos de ejemplo |
| `docs/` | Explicaciones teóricas y análisis de complejidad |

## Ejecución rápida

```bash
python src/bfs_anim_color.py
python src/maze_solver.py --algo astar --file examples/simple.txt
```

Requiere Python ≥ 3.8 y opcionalmente `colorama` para colores en Windows:
```bash
pip install colorama
```
