"""
Unit tests for Banker's Resource-Request Algorithm
"""

import unittest
from src.models import BankerState
from src.banker import BankerEngine


class TestRequestAlgorithm(unittest.TestCase):

    def setUp(self):
        self.state = BankerState(
            num_processes=5,
            num_resources=3,
            available=[3, 3, 2],
            max_matrix=[
                [7, 5, 3],
                [3, 2, 2],
                [9, 0, 2],
                [2, 2, 2],
                [4, 3, 3],
            ],
            allocation_matrix=[
                [0, 1, 0],
                [2, 0, 0],
                [3, 0, 2],
                [2, 1, 1],
                [0, 0, 2],
            ],
        )
        self.engine = BankerEngine(self.state)

    def test_valid_request_granted(self):
        # P1 requests [1, 0, 2]
        # P1 Need is [1, 2, 2], Available is [3, 3, 2]
        result = self.engine.request_resources(1, [1, 0, 2])
        self.assertTrue(result.granted)
        self.assertEqual(result.status_code, "GRANTED")
        self.assertEqual(self.engine.state.available, [2, 3, 0])
        self.assertEqual(self.engine.state.allocation_matrix[1], [3, 0, 2])
        self.assertEqual(self.engine.state.need_matrix[1], [0, 2, 0])

    def test_request_exceeding_need(self):
        # P0 need is [7, 4, 3]. Request [0, 5, 0] exceeds need in B (4)
        result = self.engine.request_resources(0, [0, 5, 0])
        self.assertFalse(result.granted)
        self.assertEqual(result.status_code, "DENIED_EXCEEDS_MAX")
        # System state must remain completely unchanged
        self.assertEqual(self.engine.state.available, [3, 3, 2])
        self.assertEqual(self.engine.state.allocation_matrix[0], [0, 1, 0])

    def test_request_exceeding_available(self):
        # P4 requests [4, 3, 1], but available is [3, 3, 2] (A: 4 > 3)
        result = self.engine.request_resources(4, [4, 3, 1])
        self.assertFalse(result.granted)
        self.assertEqual(result.status_code, "DENIED_INSUFFICIENT_AVAILABLE")
        # System state must remain unchanged
        self.assertEqual(self.engine.state.available, [3, 3, 2])

    def test_request_leading_to_unsafe_state_rolled_back(self):
        # Create a state where a request passes Need and Available checks,
        # but granting it would leave no safe sequence.
        # Suppose P0 requests [3, 3, 0]
        # Need is [7, 4, 3] -> ok; Available is [3, 3, 2] -> ok.
        # After allocation: Available = [0, 0, 2].
        # Can P1 ([1, 2, 2]) run? No (0 < 1).
        # Can P3 ([0, 1, 1]) run? No (0 < 1).
        # No process can run! Unsafe state.
        result = self.engine.request_resources(0, [3, 3, 0])
        self.assertFalse(result.granted)
        self.assertEqual(result.status_code, "DENIED_UNSAFE_STATE")
        # Ensure rollback was executed
        self.assertEqual(self.engine.state.available, [3, 3, 2])
        self.assertEqual(self.engine.state.allocation_matrix[0], [0, 1, 0])

    def test_resource_release(self):
        # P2 releases [1, 0, 1] of its [3, 0, 2] allocation
        success, msg = self.engine.release_resources(2, [1, 0, 1])
        self.assertTrue(success)
        self.assertEqual(self.engine.state.allocation_matrix[2], [2, 0, 1])
        self.assertEqual(self.engine.state.available, [4, 3, 3])

    def test_resource_release_exceeding_held(self):
        # P0 holds [0, 1, 0], trying to release [1, 0, 0]
        success, msg = self.engine.release_resources(0, [1, 0, 0])
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
