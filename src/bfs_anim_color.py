# bfs_anim_color.py
# Animación BFS con colores ANSI. Usa colorama si está disponible (Windows).
import time, os, sys
from collections import deque

try:
    from colorama import init as colorama_init
    colorama_init()
except Exception:
    pass

# Colores ANSI
RESET = "\033[0m"
BOLD  = "\033[1m"
FG_VIS = "\033[34m"   # azul para visitado
FG_FRONT = "\033[32m" # verde para frontera
FG_GOAL = "\033[31m"  # rojo para meta
FG_START = "\033[35m" # magenta para inicio
FG_WALL = "\033[90m"  # gris para muro

maze = [
    list("#####"),
    list("#S..#"),
    list("#.#.#"),
    list("#..G#"),
    list("#####"),
]

start, goal = (1, 1), (3, 3)

def vecinos(r, c):
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r+dr, c+dc
        if maze[nr][nc] != '#':
            yield nr, nc

def pinta_celda(ch, r, c, visited, frontier):
    if (r, c) == start:
        return FG_START + 'S' + RESET
    if (r, c) == goal:
        return FG_GOAL + 'G' + RESET
    if ch == '#':
        return FG_WALL + '#' + RESET
    if (r, c) in frontier:
        return FG_FRONT + '*' + RESET
    if (r, c) in visited:
        return FG_VIS + '·' + RESET
    return ch

def mostrar(grid, frontier, visited, paso, delay=0.5):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{BOLD}BFS por capas. Paso {paso}{RESET}\n")
    for r, row in enumerate(grid):
        line = []
        for c, ch in enumerate(row):
            line.append(pinta_celda(ch, r, c, visited, set(frontier)))
        print("".join(line))
    print("\nLeyenda: "
          f"{FG_FRONT}* frontera{RESET}, "
          f"{FG_VIS}· visitado{RESET}, "
          f"{FG_START}S inicio{RESET}, "
          f"{FG_GOAL}G meta{RESET}")
    time.sleep(delay)

def reconstruir(came, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(came[path[-1]])
    path.reverse()
    return path

def bfs_animado(delay=0.5):
    queue = deque([start])
    visited = {start}
    came = {}
    paso = 0
    while queue:
        mostrar(maze, list(queue), visited, paso, delay)
        next_queue = deque()
        while queue:
            u = queue.popleft()
            if u == goal:
                return came, paso
            for v in vecinos(*u):
                if v not in visited:
                    visited.add(v)
                    came[v] = u
                    next_queue.append(v)
        queue = next_queue
        paso += 1
    return came, paso

def dibuja_camino(path):
    grid = [row[:] for row in maze]
    for r, c in path[1:-1]:
        grid[r][c] = '*'
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{BOLD}Camino final encontrado ({len(path)-1} pasos):{RESET}\n")
    for r, row in enumerate(grid):
        line = []
        for c, ch in enumerate(row):
            if (r,c) == start:
                line.append(FG_START + 'S' + RESET)
            elif (r,c) == goal:
                line.append(FG_GOAL + 'G' + RESET)
            elif ch == '#':
                line.append(FG_WALL + '#' + RESET)
            elif ch == '*':
                line.append(FG_FRONT + '*' + RESET)
            else:
                line.append(ch)
        print("".join(line))

if __name__ == "__main__":
    # Parámetro opcional: delay en segundos entre fotogramas.
    delay = 0.5
    if len(sys.argv) >= 2:
        try:
            delay = float(sys.argv[1])
        except ValueError:
            pass
    came, _ = bfs_animado(delay=delay)
    if goal in came or goal == start:
        path = reconstruir(came, start, goal)
        dibuja_camino(path)
    else:
        print("No hay camino.")
