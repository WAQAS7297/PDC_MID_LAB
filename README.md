# 🚀 PDC Mid Lab Exam – Parallel & Distributed Image Processing

**Student:** Waqas Ramzan  
**Course:** Parallel and Distributed Computing  
**Project Type:** Sequential vs Parallel vs Distributed Performance Evaluation

---

## 📌 Project Overview

This project demonstrates how **parallel and distributed computing** improve performance compared to traditional **sequential** execution.  
The task processes an image dataset (resizing + watermarking) using:

| Method      | Technology Used   | Output Directory      |
|------------|-----------------|---------------------|
| Sequential | Single CPU       | `output_seq/`        |
| Parallel   | Multiprocessing  | `output_parallel/`   |
| Distributed| Simulated 2-Node | `output_distributed/`|

---

## 📊 Performance Comparison Table

| Method      | Workers/Nodes | Time (s) | Speedup |
|------------|---------------|----------|---------|
| Sequential | 1             | 0.57     | 1.00x   |
| Parallel   | 2 Workers     | 0.48     | 1.58x   |
| Parallel   | 4 Workers     | 0.34     | 2.24x   |
| Parallel   | **8 Workers (Best)** | 0.31 | 2.45x   |
| Parallel   | 24 Workers    | 0.51     | 1.49x   |
| Distributed| 2 Nodes       | 0.31     | 25.32x  |

**Best Configuration:** 8 Workers – provides **maximum CPU utilization** and best runtime.

---

## 🧠 Performance Discussion

Parallel processing significantly improves performance by utilizing **multiple CPU cores simultaneously**, reducing total execution time compared to sequential execution.

However, some bottlenecks still remain:

- Overhead from **process creation**  
- **File I/O operations** while reading/writing images  
- Diminishing speedup after 8 workers due to **CPU saturation and context switching**

Distributed processing showed the highest performance improvement because the workload was **evenly split** across two logical nodes, minimizing execution time.

---

## ✅ Key Learning Outcomes

- Sequential → Slow but simple  
- Parallel → Faster using multiprocessing  
- Distributed → Best performance for large workloads  

---

## 🗂 Included Files


---

## 🛠 How to Run

```bash
python sequential_process.py
python parallel_process.py
python distributed_sim.py




