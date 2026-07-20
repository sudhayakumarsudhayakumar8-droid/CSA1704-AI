import heapq
import math
from collections import deque

def display_menu():
    print("\n" + "="*50)
    print("      ARTIFICIAL INTELLIGENCE ASSESSMENT SOLVER      ")
    print("="*50)
    print("1. Question 1: Water Jug Problem (BFS)")
    print("2. Question 2: Mars Rover PEAS & Architecture Analysis")
    print("3. Question 3: 8-Queens Problem (Backtracking)")
    print("4. Question 4: OLA Cab Booking Agent Simulation")
    print("5. Question 5: Uniform Cost Search (UCS) Network Solver")
    print("6. Exit")
    print("="*50)

# --- QUESTION 1: WATER JUG ---
def solve_water_jug():
    print("\n--- Running Water Jug Problem Solver ---")
    initial_state = (0, 0)
    goal_jug4 = 2
    
    queue = deque([(initial_state, [initial_state])])
    visited = set([initial_state])
    
    while queue:
        (j4, j3), path = queue.popleft()
        
        if j4 == goal_jug4:
            print(f"\nGoal Reached! Total Steps: {len(path)-1}")
            for i, state in enumerate(path):
                print(f"Step {i}: 4-Gal Jug = {state[0]}g, 3-Gal Jug = {state[1]}g")
            return
            
        moves = [
            (4, j3),                             # Fill 4-gal
            (j4, 3),                             # Fill 3-gal
            (0, j3),                             # Empty 4-gal
            (j4, 0),                             # Empty 3-gal
            (4, j3 - (4 - j4)) if j4 + j3 >= 4 else (j4 + j3, 0), # Pour 3 -> 4
            (j4 - (3 - j3), 3) if j4 + j3 >= 3 else (0, j4 + j3)  # Pour 4 -> 3
        ]
        
        for next_state in moves:
            next_j4, next_j3 = next_state
            if 0 <= next_j4 <= 4 and 0 <= next_j3 <= 3:
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [next_state]))

# --- QUESTION 2: MARS ROVER PEAS ---
def show_mars_rover_peas():
    print("\n--- Mars Rover PEAS & Architecture Analysis ---")
    print("\n[P] PERCEPTS:")
    print("  - Cameras (images, depth maps), Infrared sensors, LiDAR range data.")
    print("  - Temperature, pressure, wind gauges, wheel slippage trackers, spectrometers.")
    
    print("\n[E] ENVIRONMENT:")
    print("  - Partially Observable, Stochastic, Sequential, Dynamic, Continuous, Single-agent.")
    
    print("\n[A] ACTIONS:")
    print("  - Steering, driving, core drilling, soil scooping, data antenna adjustment.")
    
    print("\n[S] PERFORMANCE MEASURE:")
    print("  - Scientific value of samples, system safety (not getting stuck), battery efficiency.")
    
    print("\n[ARCHITECTURE] RECOMMENDED:")
    print("  - Goal-Based / Utility-Based Hybrid Agent.")
    print("  - Reason: Earth-to-Mars latency is high. The rover must independently calculate the")
    print("    safest, highest-yield paths without waiting for immediate human reflex commands.")

# --- QUESTION 3: 8-QUEENS ---
def is_queen_safe(board, row, col):
    for i in range(col):
        if board[row][i] == 1: return False
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1: return False
    for i, j in zip(range(row, 8, 1), range(col, -1, -1)):
        if board[i][j] == 1: return False
    return True

def solve_8_queens_util(board, col):
    if col >= 8: return True
    for i in range(8):
        if is_queen_safe(board, i, col):
            board[i][col] = 1
            if solve_8_queens_util(board, col + 1): return True
            board[i][col] = 0
    return False

def run_8_queens():
    print("\n--- Running 8-Queens Problem Solver ---")
    board = [[0]*8 for _ in range(8)]
    if solve_8_queens_util(board, 0):
        for row in board:
            print(" ".join("Q" if x == 1 else "." for x in row))
    else:
        print("No solution found.")

# --- QUESTION 4: OLA CAB AGENT ---
class CabAgent:
    def solve_cab_routing(self, origin, destination, user_preference):
        print(f"\n--- OLA Cab Agent Simulation ---")
        print(f"Goal Request: {origin} -> {destination} | Tier: {user_preference.upper()}")
        
        drivers = [
            {"name": "Driver_1", "x": 2, "y": 3, "type": "mini"},
            {"name": "Driver_2", "x": 8, "y": 9, "type": "sedan"},
            {"name": "Driver_3", "x": 1, "y": 1, "type": "prime"},
            {"name": "Driver_4", "x": 5, "y": 4, "type": "mini"},
        ]
        
        eligible = [d for d in drivers if d["type"] == user_preference.lower()]
        if not eligible:
            print("Result: Failure. No matching cabs found nearby.")
            return

        selected_driver = min(eligible, key=lambda d: math.sqrt((d["x"]-origin[0])**2 + (d["y"]-origin[1])**2))
        print(f"Matched: {selected_driver['name']} ({selected_driver['type']})")
        print(f"Action Sequence: [Dispatch Cab] -> [Navigate via optimal traffic route] -> [Arrive]")

# --- QUESTION 5: UNIFORM COST SEARCH ---
def run_ucs():
    print("\n--- Running Uniform Cost Search (UCS) ---")
    graph = {
        'S': {'A': 1, 'G': 12},
        'A': {'B': 3, 'C': 1},
        'B': {'D': 3},
        'C': {'D': 1, 'G': 2},
        'D': {'G': 3},
        'G': {}
    }
    
    pq = [(0, 'S', ['S'])]
    visited = set()
    
    while pq:
        cost, current, path = heapq.heappop(pq)
        print(f"Evaluating node '{current}' | Cumulative path cost: {cost}")
        
        if current == 'G':
            print("\n" + "="*40)
            print(f"OPTIMAL PATH FOUND: {' -> '.join(path)}")
            print(f"TOTAL MINIMUM COST: {cost}")
            print("="*40)
            return
            
        if current not in visited:
            visited.add(current)
            for neighbor, edge_cost in graph.get(current, {}).items():
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + edge_cost, neighbor, path + [neighbor]))

# --- MAIN EXECUTION ---
def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            solve_water_jug()
        elif choice == '2':
            show_mars_rover_peas()
        elif choice == '3':
            run_8_queens()
        elif choice == '4':
            agent = CabAgent()
            # Simulating a user at coordinates (0,0) traveling to (10,10) picking a 'mini' cab
            agent.solve_cab_routing((0, 0), (10, 10), "mini")
        elif choice == '5':
            run_ucs()
        elif choice == '6':
            print("\nExiting Program. Good luck with your assignment!")
            break
        else:
            print("\nInvalid choice. Please select a number between 1 and 6.")

if __name__ == "__main__":
    main()
