"""
U1_A1 - Analytical Problem Solving
Course: Artificial Intelligence (CSA17)

This single script implements runnable solutions for all five problems
in the assessment:
    1. Water Jug Problem            - solved with BFS over (jug1, jug2) states
    2. Mars Rover Agent              - simulated utility-based agent
    3. 8-Queens Problem              - solved with backtracking search
    4. OLA Cab Booking Agent         - simulated goal-based agent
    5. Uniform Cost Search (UCS)     - least-cost path on a warehouse graph

Run with:  python Python_Code.py
"""

from collections import deque
import heapq


def banner(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------------
# 1. WATER JUG PROBLEM  (BFS state-space search)
# ---------------------------------------------------------------------
def water_jug_bfs(cap1=4, cap2=3, target=2):
    """Find a shortest sequence of actions that leaves `target` gallons
    in the jug of capacity `cap1`, starting from (0, 0)."""
    start = (0, 0)
    visited = {start}
    queue = deque([(start, [])])

    while queue:
        (j1, j2), path = queue.popleft()

        if j1 == target:
            return path

        next_states = [
            (cap1, j2, "Fill jug1"),
            (j1, cap2, "Fill jug2"),
            (0, j2, "Empty jug1"),
            (j1, 0, "Empty jug2"),
            (max(0, j1 - (cap2 - j2)), min(cap2, j1 + j2), "Pour jug1 -> jug2"),
            (min(cap1, j1 + j2), max(0, j2 - (cap1 - j1)), "Pour jug2 -> jug1"),
        ]

        for nj1, nj2, action in next_states:
            state = (nj1, nj2)
            if state not in visited:
                visited.add(state)
                queue.append((state, path + [(action, nj1, nj2)]))

    return None


def run_water_jug():
    banner("1. WATER JUG PROBLEM")
    result = water_jug_bfs(4, 3, 2)
    print("Goal: exactly 2 gallons in the 4-gallon jug\n")
    for step_no, (action, j1, j2) in enumerate(result, start=1):
        print(f"Step {step_no}: {action:<20} -> (4G={j1}, 3G={j2})")
    final_action, final_j1, final_j2 = result[-1]
    print(f"\nFinal state reached: (4-gallon jug = {final_j1}, 3-gallon jug = {final_j2})")


# ---------------------------------------------------------------------
# 2. MARS ROVER AGENT  (grid-based simulation, utility-based decisions,
#    BFS pathfinding toward the nearest unexplored sample)
# ---------------------------------------------------------------------
GRID = [
    ["plain",    "plain",    "obstacle", "plain",    "rock"],
    ["plain",    "obstacle", "plain",    "plain",    "plain"],
    ["rock",     "plain",    "plain",    "obstacle", "plain"],
    ["plain",    "plain",    "obstacle", "plain",    "rock"],
    ["plain",    "plain",    "plain",    "plain",    "plain"],
]
ROWS, COLS = len(GRID), len(GRID[0])
START_POS = (0, 0)
MAX_STEPS = 25
LOW_BATTERY_THRESHOLD = 25


def in_bounds(pos):
    r, c = pos
    return 0 <= r < ROWS and 0 <= c < COLS


def is_walkable(pos):
    r, c = pos
    return GRID[r][c] != "obstacle"


def neighbors(pos):
    r, c = pos
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nxt = (r + dr, c + dc)
        if in_bounds(nxt) and is_walkable(nxt):
            yield nxt


def bfs_shortest_path(start, goal):
    """Breadth-first search for the shortest obstacle-free path from
    start to goal on the grid. Returns the path as a list of positions,
    or None if unreachable."""
    if start == goal:
        return [start]
    visited = {start}
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        for nxt in neighbors(node):
            if nxt not in visited:
                new_path = path + [nxt]
                if nxt == goal:
                    return new_path
                visited.add(nxt)
                queue.append(new_path)
    return None


class MarsRoverAgent:
    """A utility-based agent that perceives its local grid neighborhood,
    scores candidate actions, and uses BFS to plan a route toward the
    nearest known sample when movement is the chosen action."""

    def __init__(self, start_pos):
        self.pos = start_pos
        self.battery = 100
        self.samples_collected = 0
        self.distance_travelled = 0
        self.collected_positions = set()
        self.data_sent = False

    def remaining_samples(self):
        return [
            (r, c)
            for r in range(ROWS)
            for c in range(COLS)
            if GRID[r][c] == "rock" and (r, c) not in self.collected_positions
        ]

    def perceive(self):
        """Build a percept dict from the current cell and its neighbors."""
        r, c = self.pos
        adjacent = {}
        for label, (dr, dc) in {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}.items():
            nxt = (r + dr, c + dc)
            if in_bounds(nxt):
                adjacent[label] = GRID[nxt[0]][nxt[1]]
            else:
                adjacent[label] = "edge"
        return {
            "position": self.pos,
            "current_terrain": GRID[r][c],
            "adjacent": adjacent,
            "battery": self.battery,
            "remaining_samples": len(self.remaining_samples()),
        }

    def utility(self, action, percept):
        """Score each candidate action from the current percept."""
        scores = {}
        scores["recharge"] = 20 if self.battery < LOW_BATTERY_THRESHOLD else 0
        scores["collect_sample"] = (
            9 if percept["current_terrain"] == "rock" and self.pos not in self.collected_positions else 0
        )
        scores["send_data"] = 7 if percept["remaining_samples"] == 0 and not self.data_sent else 0
        # Moving is useful whenever samples remain and battery allows travel
        scores["move_toward_sample"] = (
            5 if percept["remaining_samples"] > 0 and self.battery >= 8 else 0
        )
        return scores.get(action, 0)

    def decide(self, percept):
        actions = ["recharge", "collect_sample", "send_data", "move_toward_sample"]
        best = max(actions, key=lambda a: self.utility(a, percept))
        return best

    def act(self, action):
        if action == "recharge":
            self.battery = min(100, self.battery + 40)
            return action, self.pos

        if action == "collect_sample":
            self.collected_positions.add(self.pos)
            self.samples_collected += 1
            self.battery -= 5
            return action, self.pos

        if action == "send_data":
            self.data_sent = True
            self.battery -= 2
            return action, self.pos

        if action == "move_toward_sample":
            targets = self.remaining_samples()
            # Pick the nearest reachable sample using BFS path length
            best_path = None
            for target in targets:
                path = bfs_shortest_path(self.pos, target)
                if path and (best_path is None or len(path) < len(best_path)):
                    best_path = path
            if best_path and len(best_path) > 1:
                self.pos = best_path[1]  # take one step along the planned route
                self.battery -= 8
                self.distance_travelled += 1
            return action, self.pos

        return action, self.pos


def run_mars_rover():
    banner("2. MARS ROVER AGENT (Utility-Based, BFS Path Planning)")
    rover = MarsRoverAgent(START_POS)
    print(f"Grid ({ROWS}x{COLS}), 'rock' = sample site, 'obstacle' = impassable:")
    for row in GRID:
        print("  " + " ".join(f"{cell[:4]:<8}" for cell in row))
    print(f"\nStart position: {START_POS}\n")

    step = 1
    while step <= MAX_STEPS:
        percept = rover.perceive()
        if rover.battery <= 0:
            print(f"Step {step}: battery depleted at {rover.pos} — mission halted.")
            break

        action = rover.decide(percept)
        action_name, new_pos = rover.act(action)

        pos_display = f"{percept['position']}->{new_pos}" if new_pos != percept["position"] else f"{percept['position']}"
        print(
            f"Step {step:>2}: pos={pos_display:<16} "
            f"terrain={percept['current_terrain']:<8} action={action_name:<18} "
            f"battery={rover.battery:>3}% samples={rover.samples_collected} "
            f"distance={rover.distance_travelled}"
        )

        if rover.data_sent and not rover.remaining_samples():
            print(f"\nAll samples collected and data transmitted after {step} steps.")
            break
        step += 1

    print(
        f"\nMission summary: samples_collected={rover.samples_collected}, "
        f"distance_travelled={rover.distance_travelled}, battery_remaining={rover.battery}%, "
        f"data_sent={rover.data_sent}"
    )
    print(
        "\nThe agent used BFS to plan the shortest obstacle-free route to the "
        "nearest unexplored sample, and a utility function to decide between "
        "moving, collecting, recharging, and transmitting data at each step — "
        "combining search-based planning with utility-based action selection."
    )



# ---------------------------------------------------------------------
# 3. 8-QUEENS PROBLEM  (backtracking search)
# ---------------------------------------------------------------------
def solve_8_queens():
    n = 8
    cols = set()
    diag1 = set()   # row - col
    diag2 = set()   # row + col
    placement = [-1] * n

    def backtrack(col):
        if col == n:
            return True
        for row in range(n):
            if row in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            placement[col] = row
            cols.add(row)
            diag1.add(row - col)
            diag2.add(row + col)

            if backtrack(col + 1):
                return True

            cols.remove(row)
            diag1.remove(row - col)
            diag2.remove(row + col)
        return False

    backtrack(0)
    return placement  # placement[col] = row


def print_board(placement):
    n = len(placement)
    for row in range(n):
        line = ""
        for col in range(n):
            line += "Q " if placement[col] == row else ". "
        print(line)


def run_8_queens():
    banner("3. 8-QUEENS PROBLEM (Backtracking Search)")
    placement = solve_8_queens()
    print("Column -> Row assignment:")
    for col, row in enumerate(placement, start=1):
        print(f"  Column {col}: Row {row + 1}")
    print("\nBoard:")
    print_board(placement)
    print("\nNo two queens attack each other in this arrangement.")


# ---------------------------------------------------------------------
# 4. OLA CAB BOOKING AGENT  (simulated goal-based agent)
# ---------------------------------------------------------------------
CAB_AVAILABILITY = {
    "Micro": True,
    "Mini": False,
    "Sedan": True,
    "Prime": True,
    "Shared": False,
}

CAB_FARE_PER_KM = {"Micro": 8, "Mini": 10, "Sedan": 14, "Prime": 20, "Shared": 6}


def ola_cab_booking(preferred_order, distance_km):
    """Goal-based agent: keeps trying cab options until the goal
    (a confirmed booking) is achieved or options run out."""
    print(f"1. Open OLA Application")
    print(f"2. Detect Current Location -> done")
    print(f"3. Input Destination -> {distance_km} km away")
    print(f"4. Display Available Cab Types: {list(CAB_AVAILABILITY.keys())}")

    for cab in preferred_order:
        print(f"5. Customer Selects Preferred Cab: {cab}")
        print(f"6. Check Cab Availability for {cab}...")
        if CAB_AVAILABILITY.get(cab, False):
            fare = CAB_FARE_PER_KM[cab] * distance_km
            print(f"7. Cab Available -> Calculate Fare = {CAB_FARE_PER_KM[cab]} x {distance_km} = {fare}")
            print(f"   Confirm Booking -> Assign Driver -> Start Trip -> Reach Destination")
            print(f'   Display "Trip Completed Successfully"')
            return cab, fare
        else:
            print(f'   Display "Selected Cab Not Available" -> trying next option\n')

    print("No cabs available from the preferred list.")
    return None, None


def run_ola_cab():
    banner("4. OLA CAB BOOKING AGENT (Goal-Based)")
    cab, fare = ola_cab_booking(["Mini", "Shared", "Sedan", "Prime"], distance_km=12)
    if cab:
        print(f"\nGoal achieved: booked a {cab} for a fare of {fare}.")


# ---------------------------------------------------------------------
# 5. UNIFORM COST SEARCH  (least-cost delivery route)
# ---------------------------------------------------------------------
GRAPH = {
    "S": [("A", 1), ("G", 12)],
    "A": [("B", 3), ("C", 1)],
    "B": [("D", 3)],
    "C": [("D", 1), ("G", 2)],
    "D": [("G", 3)],
    "G": [],
}


def uniform_cost_search(graph, start, goal):
    frontier = [(0, start, [start])]
    visited = {}

    while frontier:
        cost, node, path = heapq.heappop(frontier)

        if node == goal:
            return path, cost

        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost

        for neighbor, step_cost in graph.get(node, []):
            new_cost = cost + step_cost
            if neighbor not in visited or new_cost < visited.get(neighbor, float("inf")):
                heapq.heappush(frontier, (new_cost, neighbor, path + [neighbor]))

    return None, float("inf")


def run_ucs():
    banner("5. UNIFORM COST SEARCH (Least-Cost Delivery Route)")
    path, cost = uniform_cost_search(GRAPH, "S", "G")
    print("Warehouse graph (node: [(neighbor, cost), ...]):")
    for node, edges in GRAPH.items():
        print(f"  {node}: {edges}")

    print(f"\nLeast-cost path: {' -> '.join(path)}")
    print(f"Total cost: {cost}")


# ---------------------------------------------------------------------
if __name__ == "__main__":
    run_water_jug()
    run_mars_rover()
    run_8_queens()
    run_ola_cab()
    run_ucs()
    print("\n" + "=" * 70)
    print("All 5 problems executed successfully.")
    print("=" * 70)
