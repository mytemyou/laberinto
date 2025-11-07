from __future__ import annotations
from collections import deque
import heapq
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Iterable, Set
import argparse
import sys
from pathlib import Path

Coord = Tuple[int, int]  # (row, col)

WALL = '#'
FREE = '.'
START = 'S'
GOAL = 'G'
PATH = '*'


def load_grid_from_text(text: str) -> Tuple[List[List[str]], Coord, Coord]:
    lines = [list(line.rstrip('\n')) for line in text.splitlines() if line.strip() != ""]
    if not lines:
        raise ValueError("El grid está vacío.")
    n_cols = len(lines[0])
    for i, row in enumerate(lines):
        if len(row) != n_cols:
            raise ValueError(f"Fila {i} con longitud {len(row)} distinta de {n_cols}.")
    start: Optional[Coord] = None
    goal: Optional[Coord] = None
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == START:
                start = (r, c)
            elif ch == GOAL:
                goal = (r, c)
            elif ch not in (WALL, FREE, START, GOAL):
                raise ValueError(f"Carácter inválido '{ch}' en ({r},{c}). Use '#', '.', 'S', 'G'.")
    if start is None or goal is None:
        raise ValueError("Faltan 'S' o 'G' en el grid.")
    return lines, start, goal


def in_bounds(grid: List[List[str]], r: int, c: int) -> bool:
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


def neighbors(grid: List[List[str]], node: Coord) -> Iterable[Coord]:
    r, c = node
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if in_bounds(grid, nr, nc) and grid[nr][nc] != WALL:
            yield (nr, nc)


def reconstruct_path(came_from: Dict[Coord, Coord], start: Coord, goal: Coord) -> List[Coord]:
    if goal not in came_from and goal != start:
        return []
    node = goal
    path = [node]
    while node != start:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path


def solve_bfs(grid: List[List[str]], start: Coord, goal: Coord) -> List[Coord]:
    """Camino más corto en número de pasos."""
    q = deque([start])
    came_from: Dict[Coord, Coord] = {}
    visited: Set[Coord] = {start}
    while q:
        u = q.popleft()
        if u == goal:
            break
        for v in neighbors(grid, u):
            if v not in visited:
                visited.add(v)
                came_from[v] = u
                q.append(v)
    return reconstruct_path(came_from, start, goal)


def solve_dfs(grid: List[List[str]], start: Coord, goal: Coord) -> List[Coord]:
    """Encuentra un camino cualquiera. No garantiza el más corto."""
    stack = [start]
    came_from: Dict[Coord, Coord] = {}
    visited: Set[Coord] = {start}
    while stack:
        u = stack.pop()
        if u == goal:
            break
        for v in neighbors(grid, u):
            if v not in visited:
                visited.add(v)
                came_from[v] = u
                stack.append(v)
    return reconstruct_path(came_from, start, goal)


def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve_astar(grid: List[List[str]], start: Coord, goal: Coord) -> List[Coord]:
    """A* con heurística Manhattan. Coste uniforme 1 por paso."""
    open_heap: List[Tuple[int, Coord]] = []
    heapq.heappush(open_heap, (0, start))
    g: Dict[Coord, int] = {start: 0}
    came_from: Dict[Coord, Coord] = {}
    closed: Set[Coord] = set()

    while open_heap:
        _, u = heapq.heappop(open_heap)
        if u in closed:
            continue
        if u == goal:
            return reconstruct_path(came_from, start, goal)
        closed.add(u)
        for v in neighbors(grid, u):
            tentative = g[u] + 1
            if tentative < g.get(v, 1_000_000_000):
                g[v] = tentative
                came_from[v] = u
                f = tentative + manhattan(v, goal)
                heapq.heappush(open_heap, (f, v))
    return []


def overlay_path(grid: List[List[str]], path: List[Coord]) -> List[List[str]]:
    out = [row[:] for row in grid]
    if not path:
        return out
    start = path[0]
    goal = path[-1]
    for r, c in path[1:-1]:
        out[r][c] = PATH
    sr, sc = start
    gr, gc = goal
    out[sr][sc] = START
    out[gr][gc] = GOAL
    return out


def render(grid: List[List[str]]) -> str:
    return "\n".join("".join(row) for row in grid)


def solve(grid: List[List[str]], start: Coord, goal: Coord, algo: str) -> List[Coord]:
    algo = algo.lower()
    if algo == "bfs":
        return solve_bfs(grid, start, goal)
    if algo == "dfs":
        return solve_dfs(grid, start, goal)
    if algo in ("astar", "a*", "a-star"):
        return solve_astar(grid, start, goal)
    raise ValueError("Algoritmo no soportado. Use: bfs, dfs, astar")


def cli(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Resolver laberintos ASCII (BFS/DFS/A*).")
    p.add_argument("--file", type=str, help="Ruta a archivo con el laberinto ASCII.")
    p.add_argument("--grid", type=str, help="Grid ASCII literal con \\n. Ignora --file si se usa.")
    p.add_argument("--algo", type=str, default="astar", choices=["bfs", "dfs", "astar"],
                   help="Algoritmo de resolución.")
    args = p.parse_args(argv)

    if args.grid:
        text = args.grid
    elif args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        example = (
            "#####\n"
            "#S..#\n"
            "#.#.#\n"
            "#..G#\n"
            "#####\n"
        )
        text = example

    grid, start, goal = load_grid_from_text(text)
    path = solve(grid, start, goal, args.algo)
    solved = overlay_path(grid, path)

    print("Entrada:\n")
    print(render(grid))
    print("\nAlgoritmo:", args.algo.upper())
    if path:
        print(f"Longitud del camino: {len(path)-1} pasos")
        print("\nSolución:\n")
        print(render(solved))
        print("\nCoordenadas del camino (row,col):")
        print(path)
        return 0
    else:
        print("No hay camino.")
        return 2


if __name__ == "__main__":
    sys.exit(cli())
