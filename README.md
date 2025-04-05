# 🔦 Bridge and Torch Problem Solver

💡 _Solving one of the most famous logic puzzles using state space search in Python_

This project implements solutions to the classic **Bridge and Torch** problem using **Breadth-First Search (BFS)**, **Uniform Cost Search (UCS)**, and **Depth-First Search with Iterative Deepening (DFS-ID)**.  
It models all possible state transitions and finds the minimal time required for all people to cross the bridge.

---

## 🧠 Problem Summary

Five people need to cross a bridge at night with only one flashlight. At most two people can cross at a time, and the flashlight must always be carried.  
Each person walks at a different speed:  
**`P1 (1 min), P2 (2 min), P5 (5 min), P10 (10 min), P15 (15 min)`**

The goal is to get everyone across in the **shortest total time**.

---

## 🚀 Features

- ✅ State-space modeling using immutable sets
- ✅ Legal move generation (operators)
- ✅ Breadth-First Search (BFS) - finds a solution, but not always optimal
- ✅ Uniform Cost Search (UCS) - **the only algorithm that guarantees the optimal solution**
- ✅ Iterative Deepening Depth-First Search (DFS-ID)
- ✅ Clean step-by-step solution output
- ✅ 🖼️ Graphical path visualization using `NetworkX`

---

## 📈 Example Visualization

The optimal path is visualized as a directed graph with labeled nodes and edge weights (time increments between states).

---

## 📊 Algorithm Comparison

| Algorithm | Finds Solution | Guarantees Optimality | Uses Path Cost | Notes                                             |
| --------- | -------------- | --------------------- | -------------- | ------------------------------------------------- |
| BFS       | ✅             | ❌                    | ❌             | Explores by depth, not cost                       |
| UCS       | ✅             | ✅                    | ✅             | Explores by lowest accumulated cost               |
| DFS-ID    | ✅             | ❌                    | ❌             | Explores by depth, can miss better-cost solutions |

---

## 🛠️ How to Run

Make sure you have Python 3 installed, then:

```bash
pip install matplotlib networkx
python bridge_and_torch.py
```
