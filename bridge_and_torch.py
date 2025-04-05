from collections import deque
from queue import PriorityQueue

# Dictionary of people and their crossing times
PEOPLE = {'P1': 1, 'P2': 2, 'P5': 5, 'P10': 10, 'P15': 15}
ALL = set(PEOPLE.keys())  # Set of all people

# Initial state values
flashlight_position = 'L'  # 'L' for left side, 'R' for right side
total_time = 0  # Time taken for crossing
DL = {'P1', 'P2', 'P5', 'P10', 'P15'}  # Everyone starts on the left
DR = set()  # Right side is initially empty
state = (DL, DR, flashlight_position, total_time)  # Full state representation


def is_goal(state):
    """Check if the goal state is reached: everyone has crossed to the right side."""
    DL, DR, pos, time_elapsed = state
    return DR == ALL


def get_next_states(state):
    """Generate all legal next states from the current state."""
    DL, DR, pos, time_elapsed = state
    next_states = []

    if pos == 'L':
        # Move two people from left to right
        for person_a in DL:
            for person_b in DL:
                if person_a != person_b:
                    new_DL = DL - {person_a, person_b}
                    new_DR = DR | {person_a, person_b}
                    crossing_time = max(PEOPLE[person_a], PEOPLE[person_b])
                    new_state = (new_DL, new_DR, 'R', time_elapsed + crossing_time)
                    next_states.append(new_state)
        # Move one person from left to right
        for person in DL:
            new_DL = DL - {person}
            new_DR = DR | {person}
            crossing_time = PEOPLE[person]
            new_state = (new_DL, new_DR, 'R', time_elapsed + crossing_time)
            next_states.append(new_state)

    else:  # pos == 'R'
        # Move two people from right to left
        for person_a in DR:
            for person_b in DR:
                if person_a != person_b:
                    new_DL = DL | {person_a, person_b}
                    new_DR = DR - {person_a, person_b}
                    crossing_time = max(PEOPLE[person_a], PEOPLE[person_b])
                    new_state = (new_DL, new_DR, 'L', time_elapsed + crossing_time)
                    next_states.append(new_state)
        # Move one person from right to left
        for person in DR:
            new_DL = DL | {person}
            new_DR = DR - {person}
            crossing_time = PEOPLE[person]
            new_state = (new_DL, new_DR, 'L', time_elapsed + crossing_time)
            next_states.append(new_state)

    return next_states


def print_solution(path):
    """Print the solution in a clear and concise format."""
    print("\n=== Solution Found ===")
    total_time = path[-1][3] if path else 0
    for i in range(1, len(path)):
        prev, curr = path[i - 1], path[i]
        prev_DL, prev_DR, prev_pos, prev_time = prev
        DL, DR, pos, time = curr
        if pos == 'R':
            move = prev_DL - DL
            direction = '→ RIGHT'
        else:
            move = prev_DR - DR
            direction = '← LEFT'
        move_str = ', '.join(sorted(move))
        step_time = time - prev_time
        print(f"Step {i}: [{move_str}] {direction} ({step_time} min)")
    print(f"\n✅ Optimal total time to cross: {total_time} minutes")


def bfs():
    """Perform Breadth-First Search to find the shortest sequence of moves."""
    start_state = (frozenset(ALL), frozenset(), 'L', 0)
    queue = deque()
    queue.append((start_state, []))
    visited = set()
    visited.add((start_state[0], start_state[1], start_state[2]))

    while queue:
        current_state, path = queue.popleft()
        if is_goal(current_state):
            return path + [current_state]

        for next_state in get_next_states(current_state):
            state_id = (frozenset(next_state[0]), frozenset(next_state[1]), next_state[2])
            if state_id not in visited:
                visited.add(state_id)
                queue.append((next_state, path + [current_state]))

    return None  # No solution found


def ucs():
    """Perform Uniform Cost Search to find the minimum time crossing sequence."""
    start_state = (frozenset(ALL), frozenset(), 'L', 0)
    queue = PriorityQueue()
    queue.put((0, start_state, []))
    visited = dict()
    visited[(start_state[0], start_state[1], start_state[2])] = 0

    while not queue.empty():
        current_time, current_state, path = queue.get()
        if is_goal(current_state):
            return path + [current_state]

        for next_state in get_next_states(current_state):
            next_time = next_state[3]
            state_id = (frozenset(next_state[0]), frozenset(next_state[1]), next_state[2])

            if state_id not in visited or next_time < visited[state_id]:
                visited[state_id] = next_time
                queue.put((next_time, next_state, path + [current_state]))

    return None


# === Run UCS ===
solution1 = ucs()
if solution1:
    print_solution(solution1)
else:
    print("❌ No solution found.")

# === Optional: Run BFS (if desired) ===
# solution2 = bfs()
# if solution2:
#     print_solution(solution2)
# else:
#     print("❌ No solution found.")
