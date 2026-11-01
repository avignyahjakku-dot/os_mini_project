"""
banker.py - Core Engine for Banker's Algorithm
Operating Systems Mini Project

Implements:
1. Banker's Safety Algorithm (O(m * n^2))
2. All Safe Sequences Discovery via Backtracking DFS
3. Resource-Request Algorithm with Automatic Rollback
4. Resource Release Functionality
5. Deadlock Detection Algorithm (for comparative analysis)
"""

from typing import List, Dict, Any, Tuple, Optional
import copy
from .models import BankerState, SafetyResult, RequestResult, SimulationStep


class BankerEngine:
    """
    Core algorithmic engine executing Dijkstra's Banker's Algorithm.
    Maintains an active BankerState and provides safety checks,
    request processing, and deadlock detection.
    """

    def __init__(self, state: BankerState):
        self.state = state

    # --------------------------------------------------------------------------
    # 1. SAFETY ALGORITHM
    # --------------------------------------------------------------------------
    def check_safety(self) -> SafetyResult:
        """
        Executes the Banker's Safety Algorithm to determine if the system
        is in a safe state. Returns a SafetyResult with step-by-step trace
        and primary safe sequence.
        """
        n = self.state.num_processes
        m = self.state.num_resources

        # 1. Initialize Work and Finish
        work = list(self.state.available)
        finish = [False] * n
        safe_sequence: List[str] = []
        steps: List[SimulationStep] = []

        step_counter = 1

        while len(safe_sequence) < n:
            found_candidate = False

            for i in range(n):
                if not finish[i]:
                    # Check if Need[i] <= Work
                    can_allocate = True
                    for j in range(m):
                        if self.state.need_matrix[i][j] > work[j]:
                            can_allocate = False
                            break

                    if can_allocate:
                        work_before = list(work)
                        # Work = Work + Allocation[i]
                        for j in range(m):
                            work[j] += self.state.allocation_matrix[i][j]
                        finish[i] = True
                        p_name = self.state.process_names[i]
                        safe_sequence.append(p_name)

                        explanation = (
                            f"Process {p_name} can be safely satisfied: "
                            f"Need {self.state.need_matrix[i]} <= Work {work_before}. "
                            f"After execution, releases {self.state.allocation_matrix[i]}, "
                            f"new Work = {list(work)}."
                        )

                        steps.append(
                            SimulationStep(
                                step_number=step_counter,
                                process_id=i,
                                process_name=p_name,
                                work_before=work_before,
                                need=list(self.state.need_matrix[i]),
                                allocation=list(self.state.allocation_matrix[i]),
                                work_after=list(work),
                                finish_state=list(finish),
                                explanation=explanation,
                            )
                        )
                        step_counter += 1
                        found_candidate = True
                        break  # restart search from process 0

            # If no candidate was found in a full pass, we cannot proceed
            if not found_candidate:
                break

        is_safe = all(finish)
        all_sequences = self.find_all_safe_sequences() if is_safe else []

        if is_safe:
            msg = (
                f"System is in a SAFE STATE. "
                f"Safe sequence: {' -> '.join(safe_sequence)}. "
                f"Total valid safe sequences: {len(all_sequences)}."
            )
        else:
            deadlocked = [
                self.state.process_names[i] for i in range(n) if not finish[i]
            ]
            msg = (
                f"System is in an UNSAFE STATE! Deadlock danger detected. "
                f"Processes unable to complete: {', '.join(deadlocked)}."
            )

        return SafetyResult(
            is_safe=is_safe,
            safe_sequence=safe_sequence if is_safe else [],
            all_safe_sequences=all_sequences,
            steps=steps,
            message=msg,
            resource_utilization=self.state.calculate_utilization(),
        )

    # --------------------------------------------------------------------------
    # 2. ALL SAFE SEQUENCES (BACKTRACKING DFS)
    # --------------------------------------------------------------------------
    def find_all_safe_sequences(self, max_limit: int = 50) -> List[List[str]]:
        """
        Finds all possible permutations of safe sequences using recursive backtracking.
        Limits to max_limit to prevent exponential explosion on very large process sets.
        """
        n = self.state.num_processes
        m = self.state.num_resources
        all_seqs: List[List[str]] = []

        def backtrack(
            current_work: List[int],
            finish_mask: List[bool],
            current_path: List[int],
        ):
            if len(all_seqs) >= max_limit:
                return

            if len(current_path) == n:
                all_seqs.append([self.state.process_names[idx] for idx in current_path])
                return

            for i in range(n):
                if not finish_mask[i]:
                    # Check Need[i] <= Work
                    can_run = True
                    for j in range(m):
                        if self.state.need_matrix[i][j] > current_work[j]:
                            can_run = False
                            break

                    if can_run:
                        # Forward step
                        finish_mask[i] = True
                        new_work = [
                            current_work[j] + self.state.allocation_matrix[i][j]
                            for j in range(m)
                        ]
                        current_path.append(i)

                        backtrack(new_work, finish_mask, current_path)

                        # Backtrack step
                        current_path.pop()
                        finish_mask[i] = False

        backtrack(list(self.state.available), [False] * n, [])
        return all_seqs

    # --------------------------------------------------------------------------
    # 3. RESOURCE-REQUEST ALGORITHM
    # --------------------------------------------------------------------------
    def request_resources(
        self, process_id: int, request: List[int]
    ) -> RequestResult:
        """
        Processes a resource request from process_id according to Banker's Algorithm:
        1. If Request[j] > Need[i][j], error: Process exceeded maximum claim.
        2. If Request[j] > Available[j], process must wait (insufficient resources).
        3. Provisionally allocate resources:
           Available = Available - Request
           Allocation[i] = Allocation[i] + Request
           Need[i] = Need[i] - Request
        4. Run Safety Algorithm on provisional state:
           - If safe: Commit changes permanently.
           - If unsafe: Rollback allocation; process must wait.
        """
        n = self.state.num_processes
        m = self.state.num_resources

        if not (0 <= process_id < n):
            raise IndexError(f"Process ID {process_id} is out of bounds (0 to {n - 1})")

        if len(request) != m:
            raise ValueError(f"Request vector length ({len(request)}) != num_resources ({m})")

        p_name = self.state.process_names[process_id]
        request = [int(x) for x in request]

        # Step 1: Request <= Need constraint
        for j in range(m):
            if request[j] < 0:
                return RequestResult(
                    granted=False,
                    status_code="DENIED_NEGATIVE_REQUEST",
                    message=f"Request contains negative quantity ({request[j]}) for resource {self.state.resource_names[j]}.",
                    process_id=process_id,
                    process_name=p_name,
                    request=request,
                )
            if request[j] > self.state.need_matrix[process_id][j]:
                return RequestResult(
                    granted=False,
                    status_code="DENIED_EXCEEDS_MAX",
                    message=(
                        f"Error: Process {p_name} requested {request[j]} of "
                        f"{self.state.resource_names[j]}, which exceeds its declared remaining Need "
                        f"({self.state.need_matrix[process_id][j]})."
                    ),
                    process_id=process_id,
                    process_name=p_name,
                    request=request,
                )

        # Step 2: Request <= Available constraint
        for j in range(m):
            if request[j] > self.state.available[j]:
                return RequestResult(
                    granted=False,
                    status_code="DENIED_INSUFFICIENT_AVAILABLE",
                    message=(
                        f"Process {p_name} must wait: Resource {self.state.resource_names[j]} requested ({request[j]}) "
                        f"exceeds currently Available instances ({self.state.available[j]})."
                    ),
                    process_id=process_id,
                    process_name=p_name,
                    request=request,
                )

        # Step 3: Provisional Allocation (Simulation)
        provisional_state = self.state.clone()
        for j in range(m):
            provisional_state.available[j] -= request[j]
            provisional_state.allocation_matrix[process_id][j] += request[j]
            provisional_state.need_matrix[process_id][j] -= request[j]

        # Step 4: Run Safety Check on Provisional State
        temp_engine = BankerEngine(provisional_state)
        safety_check = temp_engine.check_safety()

        if safety_check.is_safe:
            # Commit the provisional state permanently
            self.state = provisional_state
            return RequestResult(
                granted=True,
                status_code="GRANTED",
                message=(
                    f"SUCCESS: Request by {p_name} GRANTED. "
                    f"System remains in a SAFE STATE with safe sequence: "
                    f"{' -> '.join(safety_check.safe_sequence)}."
                ),
                process_id=process_id,
                process_name=p_name,
                request=request,
                safety_result=safety_check,
                state_after=self.state.to_dict(),
            )
        else:
            # Rollback: Do not alter self.state
            return RequestResult(
                granted=False,
                status_code="DENIED_UNSAFE_STATE",
                message=(
                    f"DENIED: Granting request by {p_name} would lead to an UNSAFE STATE "
                    f"(potential deadlock). Request denied, process must wait. State rolled back."
                ),
                process_id=process_id,
                process_name=p_name,
                request=request,
                safety_result=safety_check,
                state_after=self.state.to_dict(),
            )

    # --------------------------------------------------------------------------
    # 4. RESOURCE RELEASE
    # --------------------------------------------------------------------------
    def release_resources(
        self, process_id: int, release: List[int]
    ) -> Tuple[bool, str]:
        """
        Releases allocated resources from process_id back to Available.
        Ensures release amount does not exceed currently held allocation.
        """
        n = self.state.num_processes
        m = self.state.num_resources

        if not (0 <= process_id < n):
            return False, f"Process ID {process_id} is out of bounds."

        p_name = self.state.process_names[process_id]
        for j in range(m):
            rel_val = release[j]
            if rel_val < 0:
                return False, f"Release quantity cannot be negative ({rel_val})."
            alloc_val = self.state.allocation_matrix[process_id][j]
            if rel_val > alloc_val:
                return False, (
                    f"Cannot release {rel_val} of {self.state.resource_names[j]}; "
                    f"process {p_name} only holds {alloc_val}."
                )

        for j in range(m):
            self.state.allocation_matrix[process_id][j] -= release[j]
            self.state.available[j] += release[j]
            self.state.need_matrix[process_id][j] += release[j]

        return True, f"Successfully released {release} from {p_name}."

    # --------------------------------------------------------------------------
    # 5. DEADLOCK DETECTION ALGORITHM (FOR COMPARISON)
    # --------------------------------------------------------------------------
    def detect_deadlock(
        self, current_requests: Optional[List[List[int]]] = None
    ) -> Tuple[bool, List[str], str]:
        """
        Implements the standard OS Deadlock Detection algorithm (Shoshani & Coffman).
        Used to demonstrate the fundamental difference between:
        - Deadlock Avoidance (Banker's: conservative, requires Max claims ahead of time)
        - Deadlock Detection (reactive, checks actual pending requests).
        """
        n = self.state.num_processes
        m = self.state.num_resources

        # If no pending requests supplied, default to current Need matrix
        req = current_requests if current_requests is not None else self.state.need_matrix

        work = list(self.state.available)
        finish = [False] * n

        # For detection: if allocation is 0, process is initially treated as finished
        for i in range(n):
            if all(self.state.allocation_matrix[i][j] == 0 for j in range(m)):
                finish[i] = True

        while True:
            found = False
            for i in range(n):
                if not finish[i]:
                    if all(req[i][j] <= work[j] for j in range(m)):
                        for j in range(m):
                            work[j] += self.state.allocation_matrix[i][j]
                        finish[i] = True
                        found = True
                        break
            if not found:
                break

        deadlocked_processes = [
            self.state.process_names[i] for i in range(n) if not finish[i]
        ]
        is_deadlocked = len(deadlocked_processes) > 0

        if is_deadlocked:
            msg = f"DEADLOCK DETECTED! Involves processes: {', '.join(deadlocked_processes)}."
        else:
            msg = "NO DEADLOCK DETECTED. All active processes can complete."

        return is_deadlocked, deadlocked_processes, msg
