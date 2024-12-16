# London Underground Journey Planner

## Overview

This project implements a journey planner for the London Underground system, leveraging advanced algorithms and data structures. It provides solutions for tasks involving shortest path calculations, histogram visualizations of journey durations, and analysis of the network under certain conditions, such as line closures.

The implementation uses Python and integrates mandatory library code from the book "Introduction to Algorithms" (4th edition) to ensure efficiency and correctness.

---

## Features

### Task 1: Journey Planner Based on Minutes

1. **Shortest Path Calculation**:

   - Shortest path calculations for a simplified tube network using automated methods.

2. **Empirical Time Complexity**:
   - Measures execution time for shortest path calculations in networks of increasing size.
   - Plots the relationship between execution time and network size.

### Task 2: Journey Planner Based on Number of Stops

1. **Shortest Path Calculation**:

   - Computes shortest paths based on the number of stops rather than time.
   - Compares paths based on time vs stops.

2. **Empirical Time Complexity**:
   - Similar analysis as Task 1 but focuses on the number of stops.

### Task 3: Histograms of Journey Duration

1. **Journey Duration (Minutes)**:

   - Calculates journey durations for all station pairs.
   - Plots a histogram of journey durations.
   - Identifies the longest path and its details.

2. **Journey Duration (Stops)**:
   - Repeats the above analysis using stops as the metric.

### Task 4: Network Optimization

1. **Line Closures**:

   - Identifies redundant line sections that can be closed while maintaining network connectivity using Minimum Spanning Tree (MST).

2. **Analysis Post-Closures**:
   - Updates the journey planner and reanalyzes the network with line closures.
   - Compares journey durations and histograms before and after closures.

---

## Project Structure

### Python Code Files

1. **Task 1a and 1b**:
   - Implements shortest path calculation for journey time and measures time complexity.
2. **Task 2a and 2b**:
   - Shortest path calculation and complexity analysis based on number of stops.
3. **Task 3a and 3b**:
   - Generates histograms for journey durations (time and stops) and identifies the longest paths.
4. **Task 4a and 4b**:
   - MST-based optimization for line closures and reanalysis of journey durations.
5. **Graph Connectivity (Extended Task 4a)**:
   - Ensures network connectivity during line closures using additional graph analysis.

### Data File

- **London Underground Data.xlsx**:
  - Contains the network data with journey times between adjacent stations.

### Book Library Code

- Provides essential algorithms (e.g., Dijkstra's, Kruskal's) used in the implementation.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hilyas6/london-underground-journey-planner.git
   cd london-underground-journey-planner
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure the dataset (`London Underground Data.xlsx`) is in the root directory.

---

## Usage

### Running Tasks

Each task is implemented as a standalone Python script. To execute a specific task:

```bash
python Task1a.py
```

### Output

- Console outputs include shortest paths, journey durations, and comparisons.
- Visualizations (e.g., histograms) are displayed using Matplotlib.

---

## Results and Insights

1. **Shortest Paths**:

   - Efficient algorithms identify the shortest paths in terms of time and stops.
   - Results align with theoretical expectations and automated computations.

2. **Network Optimization**:

   - MST analysis highlights line sections that can be safely removed.
   - The reduced network maintains connectivity while potentially improving efficiency.

3. **Histograms**:
   - Visual distributions of journey durations reveal trends and bottlenecks in the network.
   - Comparison pre- and post-line closures provides actionable insights.

---

## References

1. **Introduction to Algorithms (4th edition)** by Thomas H. Cormen et al.
2. Lecture slides and course material from the COMP1828 module.
3. Transport for London (TfL) map and data resources.

---

## Acknowledgments

This project was developed as part of the COMP1828 coursework by the following group members:

- **Hisole, Jazmyne (Group Leader)**
- **Khan, Hamza Ali**
- **Ilyas, Hanzla**
- **Petsallari, Panagiotis**
- **Saeed, Landa**
- **Pingili, Ravi Teja**

---

## License

This project is for academic purposes and follows the guidelines of the University of Greenwich.
