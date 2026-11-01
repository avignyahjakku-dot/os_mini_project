# OPERATING SYSTEMS MINI PROJECT REPORT

**Course Name:** Operating Systems (CSE-301)  
**Project Topic 11:** Banker's Algorithm for Deadlock Avoidance and Resource-Allocation Verification  
**Academic Year:** 2026–2027 | **Semester:** V | **Section:** CSE-A  

**Team Members & PRN:**
1. **Avignya Reddy Jakku** — PRN: `25070721024`
2. **Aapti Reddy Erragunta** — PRN: `25070721018`
3. **Ahila Meghana** — PRN: `25070721002`
4. **Krithika Reddy** — PRN: `25070721062`

**Faculty Guide:** Prof. Bibhu Prasad Sahu (Faculty of Operating Systems, Department of CSE)  
**Head of Department:** Dr. Suryanarayana (Head of Department, Department of CSE)  

---

## CERTIFICATE OF APPROVAL
This is to certify that the mini project entitled **"Banker's Algorithm for Deadlock Avoidance and Resource-Allocation Verification"** is a bona fide record of work carried out by **Avignya Reddy Jakku (PRN: 25070721024)**, **Aapti Reddy Erragunta (PRN: 25070721018)**, **Ahila Meghana (PRN: 25070721002)**, and **Krithika Reddy (PRN: 25070721062)** in partial fulfillment of the requirements for the award of the Degree of *Bachelor of Technology in Computer Science and Engineering* during the academic session 2026–2027.

```
_________________________                 _________________________
Prof. Bibhu Prasad Sahu                   Dr. Suryanarayana
Faculty Guide (Operating Systems)         Head of Department
Department of CSE                         Department of CSE
```

---

## STUDENT DECLARATION
We hereby declare that the project work presented in this mini-project report is an authentic record of our original work completed under the guidance of our faculty guide **Prof. Bibhu Prasad Sahu**, Department of Computer Science & Engineering. All citations, literature sources, and algorithmic formulations have been properly referenced in accordance with standard academic integrity guidelines.

**Team Members:**
- Avignya Reddy Jakku (25070721024)
- Aapti Reddy Erragunta (25070721018)
- Ahila Meghana (25070721002)
- Krithika Reddy (25070721062)

---

## ACKNOWLEDGEMENT
We express our profound gratitude to our faculty guide **Prof. Bibhu Prasad Sahu** and our Head of Department **Dr. Suryanarayana**, Department of Computer Science & Engineering, for providing essential academic guidance, facilities, and encouragement throughout this Operating Systems mini project.

---

## ABSTRACT
In modern multiprogrammed computer operating systems, deadlocks present a critical concurrency hazard where a set of processes remain indefinitely blocked because each process holds resources while awaiting others held by peers in a closed circular chain. While deadlock prevention imposes rigid, throughput-degrading restrictions and deadlock detection is inherently reactive, deadlock avoidance provides a dynamic, mathematically sound balance. Dijkstra's Banker's Algorithm simulates resource allocations provisionally to ensure that the system never enters an unsafe state.

This project delivers an end-to-end, production-ready simulation and verification suite for the Banker's Algorithm supporting arbitrary processes and resource types. The platform incorporates:
1. A rigorous **Safety Algorithm** verifying whether safe execution sequences exist with step-by-step trace accounting;
2. A complete **Resource-Request Algorithm** executing automated provisional allocation and state rollback upon unsafe conditions;
3. An **All-Sequence Backtracking Depth-First Search** engine discovering all topological execution paths;
4. **Dual Interfaces**: a color-coded command-line interface (CLI) and a modern responsive Web Dashboard;
5. Cross-language production implementations in **Python 3**, **C++17**, and **ANSI C99**.

---

## TABLE OF CONTENTS
- [1. Introduction](#1-introduction)
  - [1.1 Concurrency and Deadlock Overview](#11-concurrency-and-deadlock-overview)
  - [1.2 The Four Coffman Deadlock Conditions](#12-the-four-coffman-deadlock-conditions)
  - [1.3 Deadlock Handling Strategies Comparison](#13-deadlock-handling-strategies-comparison)
  - [1.4 Banker's Algorithm Principles](#14-bankers-algorithm-principles)
- [2. Problem Statement and Objectives](#2-problem-statement-and-objectives)
- [3. Literature Survey and Existing Systems](#3-literature-survey-and-existing-systems)
- [4. Requirements and Tool Specifications](#4-requirements-and-tool-specifications)
- [5. System Design and Methodology](#5-system-design-and-methodology)
  - [5.1 System Architecture](#51-system-architecture)
  - [5.2 Mathematical Formalism and Data Structures](#52-mathematical-formalism-and-data-structures)
  - [5.3 Safety Algorithm Flow and Pseudocode](#53-safety-algorithm-flow-and-pseudocode)
  - [5.4 Resource-Request Algorithm and Rollback](#54-resource-request-algorithm-and-rollback)
- [6. Implementation Details](#6-implementation-details)
- [7. Testing, Verification, and Experimental Results](#7-testing-verification-and-experimental-results)
  - [7.1 Test Case 1: Silberschatz Textbook Baseline](#71-test-case-1-silberschatz-textbook-baseline)
  - [7.2 Test Case 2: Unsafe Deadlock State](#72-test-case-2-unsafe-deadlock-state)
  - [7.3 Test Case 3: Valid Request Grant](#73-test-case-3-valid-request-grant)
  - [7.4 Test Case 4: Invalid Request Rejection and Rollback](#74-test-case-4-invalid-request-rejection-and-rollback)
  - [7.5 Test Case 5: Boundary and Stress Testing](#75-test-case-5-boundary-and-stress-testing)
- [8. Discussion and Complexity Analysis](#8-discussion-and-complexity-analysis)
  - [8.1 Algorithmic Time and Space Complexity](#81-algorithmic-time-and-space-complexity)
  - [8.2 Resource Utilization Metrics](#82-resource-utilization-metrics)
  - [8.3 Comparison of Deadlock Strategies](#83-comparison-of-deadlock-strategies)
- [9. Conclusion and Future Scope](#9-conclusion-and-future-scope)
- [References](#references)
- [Appendix: Project Source Code Listings](#appendix)

---

## 1. Introduction

### 1.1 Concurrency and Deadlock Overview
In modern multiprogrammed operating systems, multiple processes execute concurrently and compete for a finite set of physical and logical resources, such as CPU cores, main memory segments, I/O devices, files, and mutex locks. When two or more processes request exclusive access to overlapping sets of resources, an undesirable condition known as a deadlock can arise. A deadlock is defined as a system state in which every process in a set is blocked, waiting for an event (typically resource acquisition) that can only be triggered by another blocked process in the same set.

### 1.2 The Four Coffman Deadlock Conditions
As established by E. G. Coffman et al. (1971), a deadlock can occur if and only if the following four conditions hold simultaneously within the operating system:
1. **Mutual Exclusion:** At least one resource must be held in a non-shareable mode; only one process may use it at a time.
2. **Hold and Wait:** A process must currently hold at least one resource while simultaneously requesting additional resources held by other processes.
3. **No Preemption:** Resources cannot be forcibly preempted from a process holding them; they can only be released voluntarily after the process finishes its task.
4. **Circular Wait:** A closed chain of processes $\{P_0, P_1, \dots, P_n\}$ must exist such that $P_0$ is waiting for a resource held by $P_1$, $P_1$ is waiting for $P_2$, and $P_n$ is waiting for a resource held by $P_0$.

### 1.3 Deadlock Handling Strategies Comparison
Operating systems handle deadlocks using one of four foundational strategies:
- **Deadlock Ignorance (Ostrich Algorithm):** Assume deadlocks never occur; reboot if frozen (used by general-purpose OS like Linux and Windows due to low frequency).
- **Deadlock Prevention:** Invalidate at least one of the four Coffman conditions statically. While safe, it causes low resource utilization and reduced system throughput.
- **Deadlock Detection and Recovery:** Allow deadlocks to occur, periodically execute a detection graph algorithm, and recover by killing processes or preempting resources.
- **Deadlock Avoidance:** Make dynamic allocation decisions based on advance knowledge of maximum resource demands, ensuring the system never enters an unsafe state.

### 1.4 Banker's Algorithm Principles
Formulated by Edsger W. Dijkstra in 1965, the Banker's Algorithm is the quintessential deadlock avoidance algorithm. The algorithm takes its name from a banking metaphor: a small-town banker manages cash credit lines for multiple clients. The banker will never allocate cash in a way that leaves the bank unable to satisfy the maximum remaining credit demand of at least one client, who can then finish their business and return all borrowed funds to the bank's reserves.

---

## 2. Problem Statement and Objectives

### 2.1 Problem Statement
Operating system resource managers face the challenge of scheduling dynamic multi-resource requests from concurrent processes without inducing deadlock states or starving active tasks. Given a system with $n$ processes and $m$ distinct resource types, the problem is to design and implement a software simulation engine that continuously validates system safety, inspects pending resource allocation requests, provisionally simulates grant outcomes, and autonomously decides whether to grant the allocation or force the requesting process to wait while rolling back provisional state changes.

### 2.2 Specific Objectives
1. Implement Dijkstra's Banker's Safety Algorithm to verify system state safety and generate safe sequences.
2. Implement the complete Resource-Request Algorithm with automatic state rollback on unsafe predictions.
3. Implement a backtracking depth-first search engine to discover all valid safe execution permutations.
4. Build dual user interfaces: a high-productivity terminal Command Line Interface (CLI) and an interactive web-based graphical dashboard.
5. Provide production-quality implementations in Python 3, modern C++17, and ANSI C.
6. Validate system behavior across textbook cases, circular deadlocks, boundary tests, and polynomial complexity benchmarks.

---

## 3. Literature Survey and Existing Systems
The study of deadlock avoidance originated with Dijkstra's pioneering paper (1965), which introduced the concept of safe states using single resource types. Habermann (1969) generalized the model to accommodate multiple resource instances. Silberschatz, Galvin, and Gagne (2018) formalized the standard modern representation of the algorithm using Available, Max, Allocation, and Need matrices, defining the $O(m \cdot n^2)$ time complexity bounds.

Existing commercial operating systems such as Linux, Windows NT/11, and macOS do not employ Banker's Algorithm for kernel thread synchronization because acquiring accurate, static declarations of maximum memory and file handle requirements in advance from arbitrary user-space applications is unfeasible in practice. However, Banker's Algorithm remains essential in specialized mission-critical environments, including hard real-time systems, aerospace embedded avionics, high-performance database transaction managers, and distributed cloud resource orchestrators where task profiles and peak resource demands are strictly bounded and contractually declared.

---

## 4. Requirements and Tool Specifications

### 4.1 Hardware Requirements
- **Processor:** Modern x86-64 / ARM64 dual-core processor (Intel Core i3/i5/i7, AMD Ryzen, or Apple Silicon).
- **RAM:** Minimum 2.0 GB (4.0 GB recommended for browser GUI).
- **Disk Storage:** Minimum 100 MB available storage.
- **Display:** Standard 1080p resolution for optimal web dashboard rendering.

### 4.2 Software and Development Tools
- **Operating System:** Windows 10/11, Linux (Ubuntu/Debian/Fedora), or macOS.
- **Primary Language:** Python 3.10+ (tested on Python 3.13).
- **Web Framework:** Flask 3.1.1 (WSGI server).
- **Frontend Architecture:** HTML5, CSS3 (Modern Flexbox & CSS Grid), ES6+ Vanilla JavaScript.
- **Systems Implementation:** Modern C++17 (g++ / Clang / MSVC) and ANSI C99.
- **Document Generation Tools:** python-docx (v1.2.0) and python-pptx (v1.0.2).
- **Testing Suite:** Python unittest framework.

---

## 5. System Design and Methodology

### 5.1 System Architecture
The project follows a modular, decoupled architecture consisting of three primary layers:
1. **Core Domain Engine (`src/models.py`, `src/banker.py`):** Houses data structures, matrix validation logic, the safety evaluation algorithm, the resource request handler, and the state rollback manager.
2. **Presentation Layer (`src/cli.py`, `web/app.py`):** Delivers dual interaction mediums—a formatted command-line interface with colorized ASCII state tables and a modern Flask-powered web UI.
3. **Verification & Benchmark Layer (`tests/`, `test_cases/`):** Automated regression test suites verifying boundary correctness and empirical time complexity scaling.

### 5.2 Mathematical Formalism and Data Structures
Let $n$ be the number of processes and $m$ be the number of resource types:
- **$\text{Available}[j]$:** Vector of length $m$. Number of available instances of resource $R_j$.
- **$\text{Max}[i][j]$:** Matrix of dimension $n \times m$. Maximum demand of process $P_i$ for resource $R_j$.
- **$\text{Allocation}[i][j]$:** Matrix of dimension $n \times m$. Number of instances of resource $R_j$ currently allocated to process $P_i$.
- **$\text{Need}[i][j] = \text{Max}[i][j] - \text{Allocation}[i][j]$:** Remaining resources process $P_i$ may request to complete execution.

### 5.3 Safety Algorithm Flow
```
1. Work = Available (vector of length m)
   Finish[i] = False for all i = 0, ..., n-1
2. Find index i such that:
   a. Finish[i] == False
   b. Need[i] <= Work
   If no such i exists, go to Step 4.
3. Work = Work + Allocation[i]
   Finish[i] = True
   Append Pi to safe_sequence
   Go to Step 2.
4. If Finish[i] == True for all i:
   System is in SAFE STATE.
   Else:
   System is in UNSAFE STATE.
```

### 5.4 Resource-Request Algorithm Flow
```
Given Request[i] from process Pi:
1. If Request[i][j] > Need[i][j] -> Error: Process exceeded maximum claim!
2. If Request[i][j] > Available[j] -> Pi must wait: Resources not available.
3. Provisional Allocation:
   Available = Available - Request[i]
   Allocation[i] = Allocation[i] + Request[i]
   Need[i] = Need[i] - Request[i]
4. Run Safety Algorithm on provisional state:
   - If Safe: Grant allocation, make state permanent.
   - If Unsafe: Rollback state changes, Pi must wait!
```

---

## 6. Implementation Details
The project implementation is structured cleanly across modular directories:
- `src/models.py`: Defines BankerState with comprehensive validation (non-negativity, dimension matching, Allocation <= Max), and dataclasses for SimulationStep, SafetyResult, and RequestResult.
- `src/banker.py`: Implements BankerEngine housing `check_safety()`, `request_resources()`, `release_resources()`, `find_all_safe_sequences()`, and comparative `detect_deadlock()`.
- `src/cli.py`: Interactive console interface featuring styled ASCII matrix tables, live request simulation, preset loading, and benchmark runner.
- `web/app.py`: Flask WSGI backend serving RESTful endpoints for real-time state manipulation and algorithm triggering.
- `web/static/`: Vanilla JS and modern CSS3 dashboard providing responsive matrix tables, animated step traces, and resource utilization bars.
- `cpp/bankers_algorithm.cpp`: High-performance C++17 implementation using vectors and stream formatting for university lab environments.

---

## 7. Testing, Verification, and Experimental Results

### 7.1 Test Case 1: Silberschatz Textbook Baseline
5 processes ($P_0 \dots P_4$), 3 resource types ($A, B, C$).  
$\text{Available} = [3, 3, 2]$.  

| Step | Process | Work (Before) | Need | Allocation Reclaimed | Work (After) | Status |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | P1 | [3, 3, 2] | [1, 2, 2] | [2, 0, 0] | [5, 3, 2] | Finished |
| 2 | P3 | [5, 3, 2] | [0, 1, 1] | [2, 1, 1] | [7, 4, 3] | Finished |
| 3 | P0 | [7, 4, 3] | [7, 4, 3] | [0, 1, 0] | [7, 5, 3] | Finished |
| 4 | P2 | [7, 5, 3] | [6, 0, 0] | [3, 0, 2] | [10, 5, 5] | Finished |
| 5 | P4 | [10, 5, 5] | [4, 3, 1] | [0, 0, 2] | [10, 5, 7] | Finished |

**Result:** System is in a SAFE STATE.  
**Primary Safe Sequence:** `P1 -> P3 -> P0 -> P2 -> P4`.  
**Total Valid Safe Permutations:** 16.

### 7.2 Test Case 2: Unsafe Deadlock State
$\text{Available} = [0, 0, 0]$. Every process still needs at least 1 resource to complete. No process can satisfy $\text{Need}[i] \le \text{Work}$.  
**Result:** System identified as UNSAFE STATE; deadlock danger flagged.

### 7.3 Test Case 3: Valid Request Grant
Process $P_1$ requests $[1, 0, 2]$.  
1. $[1, 0, 2] \le \text{Need}[1] = [1, 2, 2]$ (Passed)
2. $[1, 0, 2] \le \text{Available} = [3, 3, 2]$ (Passed)
3. Provisional Available becomes $[2, 3, 0]$. Safety algorithm executed: valid safe sequence found.  
**Outcome:** `GRANTED`. State updated permanently.

### 7.4 Test Case 4: Invalid Request Rejection and Rollback
1. **Exceeding Max Claim:** $P_0$ requests $[0, 6, 0]$ when Need is $[7, 4, 3]$. Status: `DENIED_EXCEEDS_MAX`.
2. **Exceeding Available:** $P_4$ requests $[4, 3, 1]$ when Available is $[3, 3, 2]$. Status: `DENIED_INSUFFICIENT_AVAILABLE`.
3. **Leading to Unsafe State:** $P_0$ requests $[3, 3, 0]$. Safety check fails; status: `DENIED_UNSAFE_STATE`. Provisional state rolled back immediately.

---

## 8. Discussion and Complexity Analysis

### 8.1 Algorithmic Time and Space Complexity
- **Time Complexity:** In the worst-case scenario, the safety algorithm scans up to $n$ processes in the first iteration, $n-1$ in the second, and so on. In each iteration, comparing the Need vector with the Work vector takes $m$ operations. Total operations:
  $$T(n, m) = m \cdot \sum_{i=1}^{n} i = m \cdot \frac{n(n+1)}{2} = O(m \cdot n^2)$$
- **Space Complexity:** Vectors $\text{Work}$ (size $m$), $\text{Finish}$ (size $n$), and temporary matrices require $O(m + n)$ auxiliary space.

### 8.2 Resource Utilization Metrics
$$\text{Utilization}(R_j) = \frac{\sum_{i=0}^{n-1} \text{Allocation}[i][j]}{\text{Total Instances of } R_j} \times 100\%$$
In baseline state: $A = 70.0\%, B = 40.0\%, C = 71.43\%$. After granting $P_1$'s request: $A = 80.0\%, B = 40.0\%, C = 100.0\%$.

### 8.3 Comparison of Deadlock Strategies
| Criterion | Deadlock Prevention | Deadlock Avoidance (Banker's) | Deadlock Detection & Recovery | Deadlock Ignorance (Ostrich) |
|---|---|---|---|---|
| **Approach** | Invalidate Coffman condition | Dynamic safety check | Periodic graph scan & kill | Do nothing |
| **Resource Utilization** | Low | High | High | Maximum |
| **Runtime Overhead** | Low (static) | Moderate ($O(m \cdot n^2)$ per request) | High during recovery | Zero |
| **Real-World Use** | Embedded systems | Real-time / DBMS | DBMS / Distributed systems | General OS (Linux/Windows) |

---

## 9. Conclusion and Future Scope
This project successfully designed, implemented, and verified an interactive Banker's Algorithm simulator. The platform guarantees deadlock-free resource allocation, provides step-by-step trace inspection, demonstrates mathematical polynomial complexity $O(m \cdot n^2)$, and offers dual interfaces (CLI and Web Dashboard) alongside multi-language implementations.

**Future Extensions:**
1. Dynamic Process Registration (runtime arrival and departure of processes).
2. Distributed Banker's Algorithm across multi-node cloud clusters.
3. Linux Kernel Module (LKM) integration for POSIX semaphores.

---

## References
1. A. Silberschatz, P. B. Galvin, and G. Gagne, *Operating System Concepts*, 10th ed. Hoboken, NJ: John Wiley & Sons, 2018.
2. E. W. Dijkstra, "Cooperatieve bank-overeenkomsten," Tech. Rep. EWD-108, Technische Hogeschool Eindhoven, Netherlands, 1965.
3. E. G. Coffman, M. J. Elphick, and A. Shoshani, "System Deadlocks," *ACM Computing Surveys*, vol. 3, no. 2, pp. 67–78, Jun. 1971.
4. A. N. Habermann, "Prevention of system deadlocks," *Communications of the ACM*, vol. 12, no. 7, pp. 373–377, Jul. 1969.
5. A. S. Tanenbaum and H. Bos, *Modern Operating Systems*, 4th ed. Boston, MA: Pearson, 2015.
6. W. Stallings, *Operating Systems: Internals and Design Principles*, 9th ed. Boston, MA: Pearson, 2018.
