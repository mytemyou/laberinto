# conditional_maze.py
# Búsqueda en laberinto con condiciones simples (llaves y puertas).
from collections import deque

def solve_conditional(grid, start, goal):
    filas, cols = len(grid), len(grid[0])
    def vecinos(r,c):
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr,c+dc
            if 0 <= nr < filas and 0 <= nc < cols and grid[nr][nc] != '#':
                yield nr,nc

    # Estado = (r, c, tiene_llave)
    start_state = (*start, False)
    q = deque([start_state])
    visited = {start_state}
    came = {}

    while q:
        r,c,k = q.popleft()
        if grid[r][c] == 'K':
            k = True
        if grid[r][c] == 'G':
            path = [(r,c,k)]
            while (r,c,k) != start_state:
                (r,c,k) = came[(r,c,k)]
                path.append((r,c,k))
            path.reverse()
            return path

        for nr,nc in vecinos(r,c):
            cell = grid[nr][nc]
            if cell == 'D' and not k:
                continue  # puerta cerrada
            ns = (nr,nc,k)
            if ns not in visited:
                visited.add(ns)
                came[ns] = (r,c,k)
                q.append(ns)
    return []

if __name__ == "__main__":
    maze = [
        list("########"),
        list("#S.K#..#"),
        list("#.#.#D.#"),
        list("#..#..G#"),
        list("########"),
    ]
    start = (1,1)
    goal = (3,6)
    path = solve_conditional(maze,start,goal)
    for (r,c,k) in path:
        if maze[r][c] not in "SGKD":
            maze[r][c] = '*'
    print("\n".join("".join(row) for row in maze))
