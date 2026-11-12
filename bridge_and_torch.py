from collections import deque
from itertools import combinations, count
from heapq import heappop, heappush
import argparse

# Dictionary of people and their crossing times
PEOPLE = {'P1': 1, 'P2': 2, 'P5': 5, 'P10': 10, 'P15': 15}
ALL = set(PEOPLE.keys())  # Set of all people

def is_goal(state):
    """Check if the goal state is reached: everyone has crossed to the right side."""
    return state[1] == ALL


def get_next_states(state):
    """Generate legal one- and two-person crossings in stable order."""
    left, right, torch, elapsed = state
    bank = left if torch == "L" else right
    travelers = sorted(bank, key=lambda p: (PEOPLE[p], p))
    for size in (2, 1):
        for group in combinations(travelers, size):
            move = frozenset(group)
            cost = max(PEOPLE[p] for p in move)
            if torch == "L":
                yield left - move, right | move, "R", elapsed + cost
            else:
                yield left | move, right - move, "L", elapsed + cost


def print_solution(path, title="Solution", *, minimum_time=False):
    """Print the solution path with optional title, formatted for clarity."""
    print(f"\n=== {title} ===")
    total_time = path[-1][3] if path else 0

    for i in range(1, len(path)):
        prev, curr = path[i - 1], path[i]
        prev_DL, prev_DR, prev_pos, prev_time = prev
        DL, DR, pos, time = curr
        if pos == 'R':
            move = prev_DL - DL
            direction = '-> RIGHT'
        else:
            move = prev_DR - DR
            direction = '<- LEFT'
        move_str = ', '.join(sorted(move))
        step_time = time - prev_time
        print(f"Step {i}: [{move_str}] {direction} ({step_time} min)")
    label = "Minimum crossing time" if minimum_time else "Route time"
    print(f"\n{label}: {total_time} minutes")


def bfs():
    """Perform Breadth-First Search to find the shortest sequence of moves.
    BFS does not consider different edge weights (times), so it does not guarantee the optimal time solution.
    """
    start_state = (frozenset(ALL), frozenset(), 'L', 0)
    queue = deque()
    queue.append((start_state, []))
    visited = set()
    visited.add((start_state[0], start_state[1], start_state[2]))

    while queue:
        current_state, path = queue.popleft()
        if is_goal(current_state):
            return path + [current_state]  # Return the path to the goal state

        for next_state in get_next_states(current_state):
            state_id = (frozenset(next_state[0]), frozenset(next_state[1]), next_state[2])
            if state_id not in visited:
                visited.add(state_id)
                queue.append((next_state, path + [current_state]))

    return None  # No solution found


def dfs_limited(state, limit, path, visited):
    """Limited-depth DFS helper."""
    if is_goal(state):
        return path + [state]

    if limit == 0:
        return None

    state_id = (frozenset(state[0]), frozenset(state[1]), state[2])
    if state_id in visited:
        return None
    visited.add(state_id)

    for next_state in get_next_states(state):
        result = dfs_limited(next_state, limit - 1, path + [state], visited.copy())
        if result:
            return result

    return None


def dfs_iterative_deepening(max_depth=100):
    """
    Iterative Deepening DFS (IDDFS).
    Tries increasing depth limits until it finds a solution or reaches max_depth.
    """
    start_state = (frozenset(ALL), frozenset(), 'L', 0)

    for depth in range(1, max_depth + 1):
        print(f"Trying depth limit: {depth}")
        visited = set()
        result = dfs_limited(start_state, depth, [], visited)
        if result:
            print(f"\nSolution found at depth {depth}")
            return result

    print("No solution found within depth limit.")
    return None


def ucs():
    """Perform Uniform Cost Search to find the minimum time crossing sequence."""
    start_state = (frozenset(ALL), frozenset(), 'L', 0)
    order = count()
    queue = [(0, next(order), start_state, [])]
    visited = dict()
    visited[(start_state[0], start_state[1], start_state[2])] = 0

    while queue:
        current_time, _, current_state, path = heappop(queue)
        if current_time != visited[current_state[:3]]:
            continue
        if is_goal(current_state):
            return path + [current_state]

        for next_state in get_next_states(current_state):
            next_time = next_state[3]
            state_id = (frozenset(next_state[0]), frozenset(next_state[1]), next_state[2])

            if state_id not in visited or next_time < visited[state_id]:
                visited[state_id] = next_time
                heappush(queue, (next_time, next(order), next_state, path + [current_state]))

    return None  # No solution found


def visualize_solution_path(solution, title, output=None):
    """Visualize the solution path using NetworkX and Matplotlib."""
    import networkx as nx
    import matplotlib
    if output:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    G = nx.DiGraph()
    for i in range(len(solution) - 1):
        curr = f"S{i}\n{sorted(solution[i][0])} → {sorted(solution[i][1])}\n{solution[i][3]}m"
        next = f"S{i+1}\n{sorted(solution[i+1][0])} → {sorted(solution[i+1][1])}\n{solution[i+1][3]}m"
        step_time = solution[i+1][3] - solution[i][3]
        G.add_edge(curr, next, label=f"{step_time}m")

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(14, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1800, font_size=9, font_weight='bold', arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)
    plt.title(title, fontsize=14)
    if output:
        plt.savefig(output, bbox_inches="tight")
    else:
        plt.show()
    plt.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Solve the five-traveler bridge and torch puzzle.")
    parser.add_argument("--algorithm", choices=("ucs", "bfs", "iddfs"), default="ucs")
    plot = parser.add_mutually_exclusive_group()
    plot.add_argument("--plot", action="store_true", help="open an interactive route figure")
    plot.add_argument("--save", metavar="PATH", help="save the route figure without opening a window")
    args = parser.parse_args(argv)
    search, title = {
        "ucs": (ucs, "Uniform-cost search"),
        "bfs": (bfs, "Breadth-first search"),
        "iddfs": (dfs_iterative_deepening, "Iterative deepening DFS"),
    }[args.algorithm]
    path = search()
    if path is None:
        parser.exit(1, "No route found.\n")
    print_solution(path, title, minimum_time=args.algorithm == "ucs")
    if args.plot or args.save:
        try:
            visualize_solution_path(path, title, args.save)
        except ImportError:
            parser.exit(2, "Plotting needs the optional packages: python -m pip install -r requirements-plot.txt\n")


if __name__ == "__main__":
    main()
