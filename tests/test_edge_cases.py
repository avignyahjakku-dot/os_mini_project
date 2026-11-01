"""
Unit tests for boundary edge cases, input validation, and deadlock detection.
"""

import unittest
from src.models import BankerState
from src.banker import BankerEngine


class TestEdgeCasesAndValidation(unittest.TestCase):

    def test_negative_available_rejected(self):
        with self.assertRaises(ValueError):
            BankerState(
                num_processes=2,
                num_resources=2,
                available=[-1, 2],
                max_matrix=[[2, 2], [2, 2]],
                allocation_matrix=[[1, 1], [0, 0]],
            )

    def test_allocation_exceeding_max_rejected(self):
        with self.assertRaises(ValueError):
            BankerState(
                num_processes=2,
                num_resources=2,
                available=[2, 2],
                max_matrix=[[2, 2], [1, 1]],
                allocation_matrix=[[3, 1], [0, 0]],  # 3 > 2!
            )

    def test_dimension_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            BankerState(
                num_processes=2,
                num_resources=3,
                available=[2, 2],  # Expected 3
                max_matrix=[[2, 2, 2], [1, 1, 1]],
                allocation_matrix=[[1, 1, 1], [0, 0, 0]],
            )

    def test_zero_needs_system(self):
        # All processes already hold their maximum demand
        state = BankerState(
            num_processes=2,
            num_resources=2,
            available=[0, 0],
            max_matrix=[[2, 2], [1, 1]],
            allocation_matrix=[[2, 2], [1, 1]],
        )
        engine = BankerEngine(state)
        result = engine.check_safety()
        self.assertTrue(result.is_safe)
        self.assertEqual(len(result.safe_sequence), 2)

    def test_deadlock_detection(self):
        # A state where P0 and P1 both hold resources and request what the other holds
        state = BankerState(
            num_processes=2,
            num_resources=2,
            available=[0, 0],
            max_matrix=[[2, 2], [2, 2]],
            allocation_matrix=[[1, 0], [0, 1]],
        )
        engine = BankerEngine(state)
        # Pending request for P0 is [0, 1] and for P1 is [1, 0]
        pending_requests = [[0, 1], [1, 0]]
        is_deadlocked, procs, msg = engine.detect_deadlock(pending_requests)
        self.assertTrue(is_deadlocked)
        self.assertEqual(set(procs), {"P0", "P1"})


if __name__ == "__main__":
    unittest.main()
