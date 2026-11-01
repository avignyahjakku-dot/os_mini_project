"""
main.py - Primary Entrypoint for Banker's Algorithm Mini Project
Operating Systems Mini Project
"""

import sys
import argparse
from src.models import BankerState
from src.banker import BankerEngine
from src.cli import InteractiveCLI, get_default_state
from src.utils import (
    load_from_json,
    load_from_text,
    format_state_table,
    format_step_trace,
    run_benchmark,
)


def main():
    parser = argparse.ArgumentParser(
        description="Banker's Algorithm for Deadlock Avoidance - OS Mini Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                        # Launch interactive terminal CLI
  python main.py --web                  # Launch modern web dashboard at http://127.0.0.1:5000
  python main.py --file test_cases/silberschatz_example.json
  python main.py --file test_cases/silberschatz_example.json --request "P1:1,0,2"
  python main.py --benchmark
        """,
    )

    parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="Path to JSON or text file containing system allocation state",
    )
    parser.add_argument(
        "--web",
        "-w",
        action="store_true",
        help="Launch the interactive Web Dashboard GUI",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port for Web Dashboard (default: 5000)",
    )
    parser.add_argument(
        "--request",
        "-r",
        type=str,
        help="Simulate a resource request, format: 'ProcessName:r1,r2,...' e.g. 'P1:1,0,2'",
    )
    parser.add_argument(
        "--benchmark",
        "-b",
        action="store_true",
        help="Run O(m * n^2) polynomial time complexity benchmark",
    )

    args = parser.parse_args()

    # Mode 1: Web Dashboard
    if args.web:
        from web.app import run_server

        print(f"Starting Banker's Algorithm Web Dashboard on http://127.0.0.1:{args.port}...")
        run_server(port=args.port)
        return

    # Mode 2: Benchmark
    if args.benchmark:
        print("=" * 70)
        print("  BANKER'S ALGORITHM TIME COMPLEXITY BENCHMARK")
        print("=" * 70)
        results = run_benchmark()
        print(f"{'Processes (n)':<15} | {'Resources (m)':<15} | {'Avg Time (ms)':<18} | {'Complexity Ops':<15}")
        print("-" * 70)
        for r in results:
            print(
                f"{r['num_processes']:<15} | {r['num_resources']:<15} | "
                f"{r['avg_time_ms']:<18.4f} | {r['operations_theoretical']:<15}"
            )
        print("-" * 70)
        return

    # Load State from File or Default
    if args.file:
        if args.file.endswith(".json"):
            state = load_from_json(args.file)
        else:
            state = load_from_text(args.file)
    else:
        state = get_default_state()

    # Mode 3: CLI Direct File Execution / Request Simulation
    if args.file or args.request:
        engine = BankerEngine(state)
        print(format_state_table(engine.state))
        print("\nChecking Initial System State Safety...")
        result = engine.check_safety()
        print(format_step_trace(result, engine.state.resource_names))
        print(f"\nSTATUS: {result.message}\n")

        if args.request:
            # Parse request: "P1:1,0,2"
            parts = args.request.split(":")
            if len(parts) != 2:
                print("Error: Request format must be 'ProcessName:r1,r2,...' e.g. 'P1:1,0,2'")
                sys.exit(1)

            p_name = parts[0].strip()
            try:
                pid = engine.state.process_names.index(p_name)
            except ValueError:
                print(f"Error: Process '{p_name}' not found. Valid: {engine.state.process_names}")
                sys.exit(1)

            req_vec = [int(x.strip()) for x in parts[1].split(",")]
            print(f"Simulating request by {p_name} for resources: {req_vec}...")
            outcome = engine.request_resources(pid, req_vec)
            print(f"\nResult Code: {outcome.status_code}")
            print(f"Outcome:     {outcome.message}")
            if outcome.granted:
                print("\n[V] Updated State Table:")
                print(format_state_table(engine.state))
        return

    # Mode 4: Interactive Menu
    cli = InteractiveCLI(state)
    cli.run()


if __name__ == "__main__":
    main()
