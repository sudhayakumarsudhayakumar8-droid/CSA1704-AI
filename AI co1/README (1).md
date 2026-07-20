# Assessment-1 — Analytical Problem Solving

**Course:** Artificial Intelligence (CSA17)
**Institution:** SIMATS Engineering

## Contents

| File | Description |
|---|---|
| `Problem.pdf` | The five problem statements as given in the assessment (Water Jug, Mars Rover, 8-Queens, OLA Cab Booking, Uniform Cost Search). |
| `Solution.pdf` | Worked solutions and answers for all five problems, with steps, tables, and diagrams. |
| `Python_Code.py` | A single runnable Python script implementing all five problems: BFS for the Water Jug problem, a simulated utility-based Mars Rover agent, backtracking search for 8-Queens, a simulated goal-based OLA Cab booking agent, and Uniform Cost Search for the warehouse routing problem. |
| `Output.png` | Terminal screenshot of `Python_Code.py` running end to end. |
| `Report.pdf` | Full combined report — problem statements, solutions, and conclusions together in one document. |
| `README.md` | This file. |

## How to Run

```bash
python3 Python_Code.py
```

Running the script executes all five problems in sequence and prints:

1. **Water Jug Problem** — shortest action sequence (via BFS) that leaves exactly 2 gallons in the 4-gallon jug.
2. **Mars Rover Agent** — a simulated utility-based agent that reacts to a sequence of percepts (terrain, obstacle distance) by choosing among sampling, moving, recharging, or transmitting data.
3. **8-Queens Problem** — a valid 8-queens placement found via backtracking search.
4. **OLA Cab Booking Agent** — a simulated goal-based agent that tries cab options in order of preference until one is available and books it.
5. **Uniform Cost Search** — the least-cost delivery route from warehouse S to warehouse G.

## Requirements

- Python 3.8+
- No external dependencies (uses only the standard library: `collections`, `heapq`).
