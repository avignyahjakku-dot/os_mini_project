"""
app.py - Flask Web Server for Banker's Algorithm Interactive Dashboard
Operating Systems Mini Project
"""

import os
from flask import Flask, render_template, request, jsonify
from src.models import BankerState
from src.banker import BankerEngine
from src.cli import get_default_state
from src.utils import load_from_json, run_benchmark

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)

# Shared active engine
current_engine = BankerEngine(get_default_state())


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state", methods=["GET"])
def get_state():
    return jsonify({
        "success": True,
        "state": current_engine.state.to_dict(),
    })


@app.route("/api/check-safety", methods=["POST"])
def check_safety():
    res = current_engine.check_safety()
    return jsonify({
        "success": True,
        "result": res.to_dict(),
        "state": current_engine.state.to_dict(),
    })


@app.route("/api/request", methods=["POST"])
def request_resources():
    data = request.get_json()
    if not data or "process_id" not in data or "request" not in data:
        return jsonify({"success": False, "message": "Missing process_id or request vector."}), 400

    try:
        pid = int(data["process_id"])
        req_vec = [int(x) for x in data["request"]]
        outcome = current_engine.request_resources(pid, req_vec)
        return jsonify({
            "success": True,
            "outcome": outcome.to_dict(),
            "state": current_engine.state.to_dict(),
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/release", methods=["POST"])
def release_resources():
    data = request.get_json()
    if not data or "process_id" not in data or "release" not in data:
        return jsonify({"success": False, "message": "Missing process_id or release vector."}), 400

    try:
        pid = int(data["process_id"])
        rel_vec = [int(x) for x in data["release"]]
        success, msg = current_engine.release_resources(pid, rel_vec)
        return jsonify({
            "success": success,
            "message": msg,
            "state": current_engine.state.to_dict(),
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/load-preset", methods=["POST"])
def load_preset():
    global current_engine
    data = request.get_json()
    preset_name = data.get("preset", "silberschatz") if data else "silberschatz"

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_cases_dir = os.path.join(base_dir, "test_cases")

    file_map = {
        "silberschatz": os.path.join(test_cases_dir, "silberschatz_example.json"),
        "unsafe": os.path.join(test_cases_dir, "unsafe_deadlock.json"),
        "multi": os.path.join(test_cases_dir, "multi_safe_sequences.json"),
        "single": os.path.join(test_cases_dir, "single_resource.json"),
        "stress": os.path.join(test_cases_dir, "boundary_stress.json"),
    }

    if preset_name in file_map and os.path.exists(file_map[preset_name]):
        current_engine = BankerEngine(load_from_json(file_map[preset_name]))
    else:
        current_engine = BankerEngine(get_default_state())

    return jsonify({
        "success": True,
        "message": f"Loaded preset '{preset_name}'.",
        "state": current_engine.state.to_dict(),
    })


@app.route("/api/custom-state", methods=["POST"])
def set_custom_state():
    global current_engine
    data = request.get_json()
    try:
        new_state = BankerState.from_dict(data)
        current_engine = BankerEngine(new_state)
        return jsonify({
            "success": True,
            "message": "Custom state loaded successfully.",
            "state": current_engine.state.to_dict(),
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route("/api/benchmark", methods=["GET"])
def get_benchmark():
    try:
        results = run_benchmark(max_processes=35, step=5)
        return jsonify({
            "success": True,
            "benchmark": results,
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def run_server(port: int = 5050):
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    run_server()
