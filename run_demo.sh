#!/usr/bin/env bash
# Quick Demo Launcher for Banker's Algorithm Project

set -e
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "========================================================================"
echo "      Banker's Algorithm for Deadlock Avoidance - OS Mini Project       "
echo "========================================================================"
echo "Select demo mode to launch:"
echo "  1) Web GUI Dashboard (Opens http://127.0.0.1:5050 in browser)"
echo "  2) Interactive Terminal CLI"
echo "  3) Quick Terminal Safety & Request Simulation"
echo "  4) C++ Native Lab Demo"
echo "  5) Time Complexity Benchmark (O(m * n^2))"
echo "  6) Run Unit Test Suite (15/15 tests)"
echo "  0) Exit"
echo "------------------------------------------------------------------------"
read -p "Enter choice [1-6, 0]: " CHOICE

case "$CHOICE" in
  1)
    echo "Starting Web Dashboard on http://127.0.0.1:5050 ..."
    python3 main.py --web --port 5050
    ;;
  2)
    python3 main.py
    ;;
  3)
    echo "Running safety check and request simulation on textbook scenario:"
    python3 main.py --file test_cases/silberschatz_example.json --request "P1:1,0,2"
    ;;
  4)
    if [ ! -f "cpp/bankers_cpp" ]; then
      echo "Compiling C++ binary..."
      cd cpp && make && cd ..
    fi
    ./cpp/bankers_cpp
    ;;
  5)
    python3 main.py --benchmark
    ;;
  6)
    python3 -m unittest discover tests
    ;;
  *)
    echo "Exiting."
    exit 0
    ;;
esac
