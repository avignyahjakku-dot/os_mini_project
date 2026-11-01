"""
models.py - Data Models and Data Validation for Banker's Algorithm
Operating Systems Mini Project
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import copy


@dataclass
class SimulationStep:
    """Represents an atomic step during the execution of the safety algorithm."""
    step_number: int
    process_id: int
    process_name: str
    work_before: List[int]
    need: List[int]
    allocation: List[int]
    work_after: List[int]
    finish_state: List[bool]
    explanation: str


@dataclass
class SafetyResult:
    """Results returned by the Banker's Safety Algorithm."""
    is_safe: bool
    safe_sequence: List[str] = field(default_factory=list)
    all_safe_sequences: List[List[str]] = field(default_factory=list)
    steps: List[SimulationStep] = field(default_factory=list)
    message: str = ""
    resource_utilization: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "safe_sequence": self.safe_sequence,
            "all_safe_sequences": self.all_safe_sequences,
            "steps": [
                {
                    "step_number": s.step_number,
                    "process_id": s.process_id,
                    "process_name": s.process_name,
                    "work_before": s.work_before,
                    "need": s.need,
                    "allocation": s.allocation,
                    "work_after": s.work_after,
                    "finish_state": s.finish_state,
                    "explanation": s.explanation,
                }
                for s in self.steps
            ],
            "message": self.message,
            "resource_utilization": self.resource_utilization,
        }


@dataclass
class RequestResult:
    """Outcome of a process resource request."""
    granted: bool
    status_code: str  # 'GRANTED', 'DENIED_EXCEEDS_MAX', 'DENIED_INSUFFICIENT_AVAILABLE', 'DENIED_UNSAFE_STATE'
    message: str
    process_id: int
    process_name: str
    request: List[int]
    safety_result: Optional[SafetyResult] = None
    state_after: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "granted": self.granted,
            "status_code": self.status_code,
            "message": self.message,
            "process_id": self.process_id,
            "process_name": self.process_name,
            "request": self.request,
            "safety_result": self.safety_result.to_dict() if self.safety_result else None,
            "state_after": self.state_after,
        }


class BankerState:
    """
    Encapsulates the state of an Operating System resource allocation system:
    - n processes: P0, P1, ..., P(n-1)
    - m resource types: R0, R1, ..., R(m-1) (or A, B, C...)
    
    Matrices:
    - Available[j]: Number of instances of resource j currently available.
    - Max[i][j]: Maximum demand of process i for resource j.
    - Allocation[i][j]: Number of instances of resource j currently allocated to process i.
    - Need[i][j] = Max[i][j] - Allocation[i][j]: Remaining resource demand for process i.
    """

    def __init__(
        self,
        num_processes: int,
        num_resources: int,
        available: List[int],
        max_matrix: List[List[int]],
        allocation_matrix: List[List[int]],
        resource_names: Optional[List[str]] = None,
        process_names: Optional[List[str]] = None,
    ):
        self.num_processes = num_processes
        self.num_resources = num_resources
        
        # Setup resource and process labels
        self.resource_names = (
            resource_names
            if resource_names and len(resource_names) == num_resources
            else [chr(65 + j) for j in range(num_resources)]  # A, B, C, ...
        )
        self.process_names = (
            process_names
            if process_names and len(process_names) == num_processes
            else [f"P{i}" for i in range(num_processes)]
        )

        self.available = [int(x) for x in available]
        self.max_matrix = [[int(x) for x in row] for row in max_matrix]
        self.allocation_matrix = [[int(x) for x in row] for row in allocation_matrix]
        self.need_matrix = self._compute_need_matrix()

        self.validate()

    def _compute_need_matrix(self) -> List[List[int]]:
        """Need[i][j] = Max[i][j] - Allocation[i][j]"""
        need = []
        for i in range(self.num_processes):
            row = []
            for j in range(self.num_resources):
                val = self.max_matrix[i][j] - self.allocation_matrix[i][j]
                row.append(val)
            need.append(row)
        return need

    def recalculate_need(self) -> None:
        """Recalculate need matrix after allocation changes."""
        self.need_matrix = self._compute_need_matrix()

    def validate(self) -> None:
        """
        Thoroughly validate state integrity:
        1. Dimension conformity
        2. Non-negativity
        3. Allocation <= Max constraint for every (process, resource)
        """
        if self.num_processes <= 0:
            raise ValueError(f"Number of processes must be > 0, got {self.num_processes}")
        if self.num_resources <= 0:
            raise ValueError(f"Number of resources must be > 0, got {self.num_resources}")

        if len(self.available) != self.num_resources:
            raise ValueError(
                f"Available vector length ({len(self.available)}) does not match num_resources ({self.num_resources})"
            )
        for j, val in enumerate(self.available):
            if val < 0:
                raise ValueError(f"Available resource '{self.resource_names[j]}' cannot be negative ({val})")

        if len(self.max_matrix) != self.num_processes:
            raise ValueError(
                f"Max matrix row count ({len(self.max_matrix)}) does not match num_processes ({self.num_processes})"
            )
        if len(self.allocation_matrix) != self.num_processes:
            raise ValueError(
                f"Allocation matrix row count ({len(self.allocation_matrix)}) does not match num_processes ({self.num_processes})"
            )

        for i in range(self.num_processes):
            if len(self.max_matrix[i]) != self.num_resources:
                raise ValueError(
                    f"Max matrix row {i} length ({len(self.max_matrix[i])}) != num_resources ({self.num_resources})"
                )
            if len(self.allocation_matrix[i]) != self.num_resources:
                raise ValueError(
                    f"Allocation matrix row {i} length ({len(self.allocation_matrix[i])}) != num_resources ({self.num_resources})"
                )

            for j in range(self.num_resources):
                alloc_val = self.allocation_matrix[i][j]
                max_val = self.max_matrix[i][j]
                if alloc_val < 0:
                    raise ValueError(
                        f"Allocation[{self.process_names[i]}][{self.resource_names[j]}] cannot be negative ({alloc_val})"
                    )
                if max_val < 0:
                    raise ValueError(
                        f"Max[{self.process_names[i]}][{self.resource_names[j]}] cannot be negative ({max_val})"
                    )
                if alloc_val > max_val:
                    raise ValueError(
                        f"Allocation exceeds Max claim for process {self.process_names[i]}, "
                        f"resource {self.resource_names[j]}: Allocation={alloc_val} > Max={max_val}"
                    )

    def total_system_resources(self) -> List[int]:
        """Total = Available + Sum of all allocated resources across processes."""
        totals = list(self.available)
        for i in range(self.num_processes):
            for j in range(self.num_resources):
                totals[j] += self.allocation_matrix[i][j]
        return totals

    def calculate_utilization(self) -> Dict[str, float]:
        """Calculates current resource utilization percentages: Allocated / Total * 100%."""
        totals = self.total_system_resources()
        utilization = {}
        for j in range(self.num_resources):
            allocated_total = sum(self.allocation_matrix[i][j] for i in range(self.num_processes))
            pct = (allocated_total / totals[j] * 100.0) if totals[j] > 0 else 0.0
            utilization[self.resource_names[j]] = round(pct, 2)
        return utilization

    def clone(self) -> "BankerState":
        """Deep copy of the current state for hypothetical state evaluation."""
        return copy.deepcopy(self)

    def to_dict(self) -> Dict[str, Any]:
        """Export state representation as a serializable dictionary."""
        return {
            "num_processes": self.num_processes,
            "num_resources": self.num_resources,
            "resource_names": self.resource_names,
            "process_names": self.process_names,
            "available": self.available,
            "max_matrix": self.max_matrix,
            "allocation_matrix": self.allocation_matrix,
            "need_matrix": self.need_matrix,
            "total_resources": self.total_system_resources(),
            "utilization": self.calculate_utilization(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BankerState":
        """Instantiate BankerState from dictionary."""
        return cls(
            num_processes=int(data["num_processes"]),
            num_resources=int(data["num_resources"]),
            available=data["available"],
            max_matrix=data["max_matrix"],
            allocation_matrix=data["allocation_matrix"],
            resource_names=data.get("resource_names"),
            process_names=data.get("process_names"),
        )
