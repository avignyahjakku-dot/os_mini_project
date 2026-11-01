"""
cli.py - Rich Command-Line Interface for Banker's Algorithm
Operating Systems Mini Project
"""

import sys
import os
from typing import Optional, List
from .models import BankerState
from .banker import BankerEngine
from .utils import (
    load_from_json,
    load_from_text,
    format_state_table,
    format_step_trace,
    generate_scenario,
    run_benchmark,
)


def get_default_state() -> BankerState:
    """Standard Silberschatz Operating System Concepts (Chapter 8) Example."""
    return BankerState(
        num_processes=5,
        num_resources=3,
        available=[3, 3, 2],
        max_matrix=[
            [7, 5, 3],  # P0
            [3, 2, 2],  # P1
            [9, 0, 2],  # P2
            [2, 2, 2],  # P3
            [4, 3, 3],  # P4
        ],
        allocation_matrix=[
            [0, 1, 0],  # P0
            [2, 0, 0],  # P1
            [3, 0, 2],  # P2
            [2, 1, 1],  # P3
            [0, 0, 2],  # P4
        ],
        resource_names=["A", "B", "C"],
        process_names=["P0", "P1", "P2", "P3", "P4"],
    )


class InteractiveCLI:
    """Full-featured interactive terminal console for the Banker's Algorithm."""

    def __init__(self, initial_state: Optional[BankerState] = None):
        self.engine = BankerEngine(initial_state or get_default_state())

    def print_banner(self) -> None:
        print("\n" + "=" * 78)
        print("   BANKER'S ALGORITHM FOR DEADLOCK AVOIDANCE - OS MINI PROJECT   ")
        print("   Advanced Simulation, Resource Allocation, and Verification    ")
        print("=" * 78)

    def display_state(self) -> None:
        print("\n" + format_state_table(self.engine.state))

    def run_safety_check(self) -> None:
        print("\n" + "-" * 78)
        print(" >>> RUNNING BANKER'S SAFETY ALGORITHM <<<")
        print("-" * 78)
        result = self.engine.check_safety()

        print(format_step_trace(result, self.engine.state.resource_names))
        print(f"\nSTATUS: {result.message}\n")

        if result.is_safe:
            print(f"Primary Safe Execution Sequence: {' -> '.join(result.safe_sequence)}")
            print(f"Total Alternative Safe Sequences Found: {len(result.all_safe_sequences)}")
        else:
            print("WARNING: The system is in an UNSAFE STATE! Any additional request could deadlock.")

    def show_all_safe_sequences(self) -> None:
        print("\n" + "-" * 78)
        print(" >>> COMPUTING ALL SAFE EXECUTION SEQUENCES (BACKTRACKING DFS) <<<")
        print("-" * 78)
        seqs = self.engine.find_all_safe_sequences(max_limit=25)
        if not seqs:
            print("NO SAFE SEQUENCES EXIST! The system is in an unsafe state.")
        else:
            print(f"Found {len(seqs)} valid sequence(s):")
            for idx, seq in enumerate(seqs, start=1):
                print(f"  [{idx:2d}] {' -> '.join(seq)}")

    def request_resources_interactive(self) -> None:
        print("\n" + "-" * 78)
        print(" >>> PROCESS RESOURCE REQUEST SIMULATION <<<")
        print("-" * 78)
        print(f"Available processes: {', '.join(self.engine.state.process_names)}")
        print(f"Resource types:      {', '.join(self.engine.state.resource_names)}")
        print(f"Currently Available: {self.engine.state.available}")

        try:
            p_input = input("Enter Process Name or Index (e.g., P1 or 1): ").strip()
            if p_input.upper().startswith("P") and p_input[1:].isdigit():
                pid = int(p_input[1:])
            else:
                pid = int(p_input)

            if not (0 <= pid < self.engine.state.num_processes):
                print(f"Error: Process index {pid} is out of bounds.")
                return

            p_name = self.engine.state.process_names[pid]
            print(f"Process {p_name} current Need: {self.engine.state.need_matrix[pid]}")
            print(f"System Available:            {self.engine.state.available}")

            req_str = input(
                f"Enter resource request for {p_name} ({self.engine.state.num_resources} integers, space or comma separated): "
            ).strip()
            
            cleaned = req_str.replace(",", " ").split()
            req_vec = [int(x) for x in cleaned]

            if len(req_vec) != self.engine.state.num_resources:
                print(f"Error: Expected {self.engine.state.num_resources} values, received {len(req_vec)}.")
                return

            print("\nEvaluating Request according to Banker's Safety Rules...")
            outcome = self.engine.request_resources(pid, req_vec)

            print(f"\nResult Code: {outcome.status_code}")
            print(f"Message:     {outcome.message}")

            if outcome.granted:
                print("\n[V] REQUEST GRANTED: System state updated successfully!")
                self.display_state()
            else:
                print("\n[X] REQUEST REJECTED: System state restored via rollback.")

        except Exception as e:
            print(f"Invalid input: {e}")

    def release_resources_interactive(self) -> None:
        print("\n" + "-" * 78)
        print(" >>> RELEASE RESOURCES FROM PROCESS <<<")
        print("-" * 78)
        try:
            p_input = input("Enter Process Name or Index (e.g., P0 or 0): ").strip()
            if p_input.upper().startswith("P") and p_input[1:].isdigit():
                pid = int(p_input[1:])
            else:
                pid = int(p_input)

            p_name = self.engine.state.process_names[pid]
            print(f"Process {p_name} currently holding: {self.engine.state.allocation_matrix[pid]}")

            rel_str = input(
                f"Enter resource amounts to release ({self.engine.state.num_resources} integers): "
            ).strip()
            cleaned = rel_str.replace(",", " ").split()
            rel_vec = [int(x) for x in cleaned]

            success, msg = self.engine.release_resources(pid, rel_vec)
            if success:
                print(f"\n[V] SUCCESS: {msg}")
                self.display_state()
            else:
                print(f"\n[X] ERROR: {msg}")
        except Exception as e:
            print(f"Invalid input: {e}")

    def compare_deadlock_detection(self) -> None:
        print("\n" + "-" * 78)
        print(" >>> DEADLOCK AVOIDANCE (BANKER'S) VS DEADLOCK DETECTION <<<")
        print("-" * 78)
        print("Analysis Concept:")
        print(" * Deadlock Avoidance (Banker's) is CONSERVATIVE: assumes processes may request their entire Need.")
        print(" * Deadlock Detection is OPTIMISTIC: checks if existing allocated state can resolve pending requests.")
        print("-" * 78)

        avoidance_res = self.engine.check_safety()
        detection_deadlocked, procs, det_msg = self.engine.detect_deadlock()

        print(f"1. Banker's Avoidance Result : {'SAFE' if avoidance_res.is_safe else 'UNSAFE (Deny non-safe requests)'}")
        print(f"2. Deadlock Detection Result : {'DEADLOCKED (' + ', '.join(procs) + ')' if detection_deadlocked else 'NO DEADLOCK'}")
        print(f"\nSummary: {det_msg}")

    def load_preset_menu(self) -> None:
        print("\nPreset Scenarios:")
        print(" 1. Silberschatz Textbook (Safe State - 5 Processes, 3 Resources)")
        print(" 2. Unsafe Deadlock Danger State (Deadlock occurs if granted)")
        print(" 3. Multiple Safe Sequences Scenario (Alternative execution orders)")
        print(" 4. Single Resource Boundary Case")
        print(" 5. Stress Test Scenario (10 Processes, 4 Resources)")

        choice = input("Select preset (1-5): ").strip()
        dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_cases")
        file_map = {
            "1": os.path.join(dir_path, "silberschatz_example.json"),
            "2": os.path.join(dir_path, "unsafe_deadlock.json"),
            "3": os.path.join(dir_path, "multi_safe_sequences.json"),
            "4": os.path.join(dir_path, "single_resource.json"),
            "5": os.path.join(dir_path, "boundary_stress.json"),
        }

        if choice in file_map and os.path.exists(file_map[choice]):
            self.engine = BankerEngine(load_from_json(file_map[choice]))
            print("\n[V] Scenario successfully loaded!")
            self.display_state()
        elif choice == "1":
            self.engine = BankerEngine(get_default_state())
            print("\n[V] Default Silberschatz scenario loaded!")
            self.display_state()
        else:
            print("Invalid preset choice or file not found.")

    def run_benchmark_ui(self) -> None:
        print("\n" + "-" * 78)
        print(" >>> RUNNING ALGORITHMIC COMPLEXITY BENCHMARK <<<")
        print(" Theoretical Complexity: O(m * n^2) operations")
        print("-" * 78)
        print(f"{'Processes (n)':<15} | {'Resources (m)':<15} | {'Empirical Time (ms)':<22} | {'Theoretical Ops':<15}")
        print("-" * 78)

        results = run_benchmark(max_processes=40, step=5)
        for r in results:
            print(
                f"{r['num_processes']:<15} | {r['num_resources']:<15} | "
                f"{r['avg_time_ms']:<22.4f} | {r['operations_theoretical']:<15}"
            )
        print("-" * 78)
        print("Empirical measurements verify quadratic scaling with process count.\n")

    def run(self) -> None:
        self.print_banner()
        self.display_state()

        while True:
            print("\n" + "=" * 50)
            print("                 MAIN MENU")
            print("=" * 50)
            print(" 1. View Current System Allocation State")
            print(" 2. Run Banker's Safety Algorithm & Step Trace")
            print(" 3. Find All Possible Safe Sequences (DFS)")
            print(" 4. Request Resources for a Process (Simulation)")
            print(" 5. Release Resources from a Process")
            print(" 6. Compare Deadlock Avoidance vs Detection")
            print(" 7. Load Preset Test Case Scenario")
            print(" 8. Load Custom State from JSON File")
            print(" 9. Generate Random State Scenario")
            print(" 10. Run Time Complexity Benchmark (O(m*n^2))")
            print(" 0. Exit")
            print("=" * 50)

            choice = input("Enter choice (0-10): ").strip()

            if choice == "1":
                self.display_state()
            elif choice == "2":
                self.run_safety_check()
            elif choice == "3":
                self.show_all_safe_sequences()
            elif choice == "4":
                self.request_resources_interactive()
            elif choice == "5":
                self.release_resources_interactive()
            elif choice == "6":
                self.compare_deadlock_detection()
            elif choice == "7":
                self.load_preset_menu()
            elif choice == "8":
                path = input("Enter path to JSON file: ").strip()
                if os.path.exists(path):
                    self.engine = BankerEngine(load_from_json(path))
                    print("\n[V] File loaded successfully!")
                    self.display_state()
                else:
                    print("[X] File does not exist.")
            elif choice == "9":
                try:
                    n = int(input("Enter number of processes (e.g. 5): ").strip())
                    m = int(input("Enter number of resources (e.g. 3): ").strip())
                    new_state = generate_scenario(n, m)
                    self.engine = BankerEngine(new_state)
                    print("\n[V] Generated scenario successfully!")
                    self.display_state()
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == "10":
                self.run_benchmark_ui()
            elif choice == "0":
                print("\nExiting Banker's Algorithm Simulation. Goodbye!")
                break
            else:
                print("Invalid selection. Please choose an option from 0 to 10.")
