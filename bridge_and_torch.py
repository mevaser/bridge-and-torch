from collections import deque


PEOPLE = {'P1': 1, 'P2': 2, 'P5': 5, 'P10': 10, 'P15': 15} # Dictionary of people and their crossing times
ALL = set(PEOPLE.keys()) # Set of all people



# Initial state
flashlight_position = 'L'  # 'L' for left side, 'R' for right side
total_time = 0 # Time taken for crossing


# Left side contains all people at the beginning
DL = {'P1', 'P2', 'P5', 'P10', 'P15'}
DR = set()

# State is a tuple: (left_side, right_side, flashlight_position, time_elapsed)
state = (DL, DR, flashlight_position, total_time)


def is_goal(state):
    """Check if the goal state is reached: everyone has crossed to the right side."""
    DL, DR, pos, time_elapsed = state
    return DR == ALL

def get_next_states(state):
    """Generate all legal next states from the current state, with debug printing."""
    DL, DR, pos, time_elapsed = state
    next_states = []

    print(f"\n=== Generating next states from ===")
    print(f"Left: {DL} | Right: {DR} | Flashlight: {pos} | Time: {time_elapsed}\n")

    if pos == 'L':
        # Moving 2 people from left to right
        for person_a in DL:
            for person_b in DL:
                if person_a != person_b:
                    new_DL = DL - {person_a, person_b}
                    new_DR = DR | {person_a, person_b}
                    crossing_time = max(PEOPLE[person_a], PEOPLE[person_b])
                    new_state = (new_DL, new_DR, 'R', time_elapsed + crossing_time)
                    next_states.append(new_state)
                    print(f"-> {person_a} and {person_b} cross to RIGHT | +{crossing_time} min")

        # Moving 1 person alone from left to right
        for person in DL:
            new_DL = DL - {person}
            new_DR = DR | {person}
            crossing_time = PEOPLE[person]
            new_state = (new_DL, new_DR, 'R', time_elapsed + crossing_time)
            next_states.append(new_state)
            print(f"-> {person} crosses alone to RIGHT | +{crossing_time} min")

    else:  # pos == 'R'
        # Moving 2 people from right to left
        for person_a in DR:
            for person_b in DR:
                if person_a != person_b:
                    new_DL = DL | {person_a, person_b}
                    new_DR = DR - {person_a, person_b}
                    crossing_time = max(PEOPLE[person_a], PEOPLE[person_b])
                    new_state = (new_DL, new_DR, 'L', time_elapsed + crossing_time)
                    next_states.append(new_state)
                    print(f"<- {person_a} and {person_b} return to LEFT | +{crossing_time} min")

        # Moving 1 person alone from right to left
        for person in DR:
            new_DL = DL | {person}
            new_DR = DR - {person}
            crossing_time = PEOPLE[person]
            new_state = (new_DL, new_DR, 'L', time_elapsed + crossing_time)
            next_states.append(new_state)
            print(f"<- {person} returns alone to LEFT | +{crossing_time} min")

    print(f"\nGenerated {len(next_states)} next states.\n")
    return next_states


for state in get_next_states(state):
    print(state)


def bfs():
    """Perform Breadth-First Search to find the shortest crossing sequence."""
    start_state = (frozenset(ALL), frozenset(), 'L', 0)
    queue = deque()
    queue.append((start_state, []))  # second item is the path to this state

    visited = set()
    visited.add((start_state[0], start_state[1], start_state[2]))  # only DL, DR, and torch position
    while queue:
        current_state, path = queue.popleft()

        if is_goal(current_state):
            return path + [current_state]
        for next_state in get_next_states(current_state):
            state_id = (frozenset(next_state[0]), frozenset(next_state[1]), next_state[2])
            if state_id not in visited:
                visited.add(state_id)
                queue.append((next_state, path + [current_state]))
    return None


# Run BFS and print the full solution path
solution = bfs()

if solution:
    print("\n=== Solution Found ===\n")
    for i, state in enumerate(solution):
        DL, DR, pos, time_elapsed = state
        print(f"Step {i}:")
        print(f"  Left side:  {sorted(DL)}")
        print(f"  Right side: {sorted(DR)}")
        print(f"  Flashlight: {pos}")
        print(f"  Time so far: {time_elapsed} minutes\n")
    print(f"✅ Total time to cross: {solution[-1][3]} minutes")
else:
    print("❌ No solution found.")
