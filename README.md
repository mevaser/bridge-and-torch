# 🔦 Bridge and Torch Problem Solver

💡 _Solving one of the most famous logic puzzles using state space search in Python_

This project implements a solution to the classic **Bridge and Torch** problem using **Breadth-First Search (BFS)**.  
It models all possible state transitions and finds the minimal time required for all people to cross the bridge.

---

## 🧠 Problem Summary

Five people need to cross a bridge at night with only one flashlight. At most two people can cross at a time, and the flashlight must always be carried.  
Each person walks at a different speed: `P1 (1 min), P2 (2 min), P5 (5 min), P10 (10 min), P15 (15 min)`.

The goal is to get everyone across in the **shortest total time**.

---

## 🚀 Features

- State-space modeling with tuples and sets
- Legal move generation based on operators
- Breadth-First Search (BFS) implementation
- Debug output to visualize all possible steps

---

## 🛠️ How to Run

Make sure you have Python 3 installed, then:

```bash
python bridge_and_torch.py
```

## Future Enhancements

- Add DFS with Iterative Deepening

- Add graphical state visualization

- Use OOP for better structure
