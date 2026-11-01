"""
utils.py - Formatting, Serialization, Scenario Generation, and Benchmarking
Operating Systems Mini Project
"""

import json
import random
import time
from typing import Dict, Any, Tuple, List, Optional
from .models import BankerState, SafetyResult


def load_from_json(filepath: str) -> BankerState:
    """Load BankerState from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return BankerState.from_dict(data)


def save_to_json(state: BankerState, filepath: str) -> None:
    """Save BankerState to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(state.to_dict(), f, indent=4)


def load_from_text(filepath: str) -> BankerState:
    """
    Load BankerState from standard OS lab plain text format:
    Line 1: num_processes num_resources
    Line 2: Available vector (m space-separated integers)
    Next n lines: Max matrix (m integers per line)
    Next n lines: Allocation matrix (m integers per line)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    if len(raw_lines) < 3:
        raise ValueError("Invalid text format: insufficient lines.")

    header = list(map(int, raw_lines[0].split()))
    num_processes, num_resources = header[0], header[1]

    available = list(map(int, raw_lines[1].split()))
    if len(available) != num_resources:
        raise ValueError(f"Available row length ({len(available)}) != {num_resources}")

    cursor = 2
    max_matrix = []
    for _ in range(num_processes):
        row = list(map(int, raw_lines[cursor].split()))
        max_matrix.append(row)
        cursor += 1

    allocation_matrix = []
    for _ in range(num_processes):
        row = list(map(int, raw_lines[cursor].split()))
        allocation_matrix.append(row)
        cursor += 1

    return BankerState(
        num_processes=num_processes,
        num_resources=num_resources,
        available=available,
        max_matrix=max_matrix,
        allocation_matrix=allocation_matrix,
    )


def format_state_table(state: BankerState) -> str:
    """
    Formats the complete system state into an ASCII table displaying
    Allocation, Max, Need, and Available vectors side-by-side.
    """
    res_names = state.resource_names
    m = state.num_resources
    res_header = " ".join(f"{r:>3}" for r in res_names)

    lines = []
    lines.append("=" * 80)
    lines.append(f"{'SYSTEM RESOURCE ALLOCATION STATE':^80}")
    lines.append("=" * 80)
    lines.append(
        f"{'Process':<9} | {'Allocation':^{len(res_header)}} | {'Max Claim':^{len(res_header)}} | {'Need':^{len(res_header)}} | {'Available':^{len(res_header)}}"
    )
    lines.append(
        f"{'':<9} | {res_header} | {res_header} | {res_header} | {res_header}"
    )
    lines.append("-" * 80)

    for i in range(state.num_processes):
        alloc_str = " ".join(f"{state.allocation_matrix[i][j]:>3}" for j in range(m))
        max_str = " ".join(f"{state.max_matrix[i][j]:>3}" for j in range(m))
        need_str = " ".join(f"{state.need_matrix[i][j]:>3}" for j in range(m))
        avail_str = (
            " ".join(f"{state.available[j]:>3}" for j in range(m))
            if i == 0
            else " " * len(res_header)
        )
        p_name = state.process_names[i]
        lines.append(f"{p_name:<9} | {alloc_str} | {max_str} | {need_str} | {avail_str}")

    lines.append("-" * 80)
    totals = state.total_system_resources()
    total_str = " ".join(f"{t:>3}" for t in totals)
    lines.append(f"Total Resources in System: [ {total_str} ]")

    util_parts = [f"{r}: {pct}%" for r, pct in state.calculate_utilization().items()]
    lines.append(f"Resource Utilization:      [ {', '.join(util_parts)} ]")
    lines.append("=" * 80)

    return "\n".join(lines)


def format_step_trace(safety_result: SafetyResult, resource_names: List[str]) -> str:
    """Formats step-by-step trace of the Safety Algorithm execution into an ASCII table."""
    lines = []
    lines.append("-" * 80)
    lines.append(f"{'SAFETY ALGORITHM EXECUTION TRACE':^80}")
    lines.append("-" * 80)
    lines.append(
        f"{'Step':<5} | {'Proc':<6} | {'Work (Before)':<16} | {'Need':<14} | {'Alloc':<14} | {'Work (After)':<16}"
    )
    lines.append("-" * 80)

    for s in safety_result.steps:
        wb_str = "[" + ", ".join(map(str, s.work_before)) + "]"
        need_str = "[" + ", ".join(map(str, s.need)) + "]"
        alloc_str = "[" + ", ".join(map(str, s.allocation)) + "]"
        wa_str = "[" + ", ".join(map(str, s.work_after)) + "]"
        lines.append(
            f"{s.step_number:<5} | {s.process_name:<6} | {wb_str:<16} | {need_str:<14} | {alloc_str:<14} | {wa_str:<16}"
        )

    lines.append("-" * 80)
    return "\n".join(lines)


def generate_scenario(
    num_processes: int = 5,
    num_resources: int = 3,
    ensure_safe: bool = True,
    seed: Optional[int] = None,
) -> BankerState:
    """
    Generates a deterministic or randomized scenario with guaranteed safety
    or intentional deadlock danger.
    """
    if seed is not None:
        random.seed(seed)

    # 1. Total system capacities (typically 5 to 15 per resource)
    total_resources = [random.randint(8, 16) for _ in range(num_resources)]

    # 2. Maximum claims for each process (must be <= total_resources)
    max_matrix = []
    for _ in range(num_processes):
        row = [random.randint(1, total_resources[j] - 1) for j in range(num_resources)]
        max_matrix.append(row)

    # 3. Allocations: initially modest so they don't exceed totals
    allocation_matrix = []
    for _ in range(num_processes):
        row = [0] * num_resources
        allocation_matrix.append(row)

    available = list(total_resources)

    # Distribute resources randomly while respecting Max and Available
    for i in range(num_processes):
        for j in range(num_resources):
            max_possible = min(max_matrix[i][j], available[j])
            if max_possible > 0:
                allocated = random.randint(0, max(1, max_possible // 2))
                allocation_matrix[i][j] = allocated
                available[j] -= allocated

    state = BankerState(
        num_processes=num_processes,
        num_resources=num_resources,
        available=available,
        max_matrix=max_matrix,
        allocation_matrix=allocation_matrix,
    )

    from .banker import BankerEngine

    engine = BankerEngine(state)
    result = engine.check_safety()

    # If user wanted safe and it's unsafe, replenish Available until safe
    if ensure_safe and not result.is_safe:
        for j in range(num_resources):
            state.available[j] += 4
        state.validate()

    return state


def run_benchmark(max_processes: int = 50, step: int = 5) -> List[Dict[str, Any]]:
    """
    Measures safety algorithm runtime over an increasing number of processes.
    Demonstrates O(m * n^2) empirical polynomial scaling.
    """
    from .banker import BankerEngine

    benchmark_data = []
    num_resources = 4

    for n in range(5, max_processes + 1, step):
        state = generate_scenario(num_processes=n, num_resources=num_resources, ensure_safe=True, seed=42 + n)
        engine = BankerEngine(state)

        # Warm up
        engine.check_safety()

        # Timed iterations
        iterations = 100
        start_time = time.perf_counter()
        for _ in range(iterations):
            engine.check_safety()
        elapsed_sec = (time.perf_counter() - start_time) / iterations

        benchmark_data.append({
            "num_processes": n,
            "num_resources": num_resources,
            "avg_time_ms": round(elapsed_sec * 1000.0, 4),
            "operations_theoretical": num_resources * (n ** 2),
        })

    return benchmark_data
