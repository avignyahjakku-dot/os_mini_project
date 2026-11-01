"""
Unit tests for Banker's Safety Algorithm
"""

import unittest
from src.models import BankerState
from src.banker import BankerEngine


class TestSafetyAlgorithm(unittest.TestCase):

    def setUp(self):
        # Silberschatz textbook state
        self.safe_state = BankerState(
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

        # Unsafe state
        self.unsafe_state = BankerState(
            num_processes=4,
            num_resources=3,
            available=[0, 0, 0],
            max_matrix=[
                [3, 2, 2],
                [2, 2, 2],
                [4, 3, 3],
                [2, 1, 1],
            ],
            allocation_matrix=[
                [2, 1, 1],
                [1, 1, 1],
                [2, 2, 1],
                [1, 0, 1],
            ],
        )

    def test_safe_state_detection(self):
        engine = BankerEngine(self.safe_state)
        result = engine.check_safety()
        self.assertTrue(result.is_safe)
        self.assertEqual(len(result.safe_sequence), 5)
        # P1 or P3 can start first
        self.assertIn(result.safe_sequence[0], ["P1", "P3"])

    def test_unsafe_state_detection(self):
        engine = BankerEngine(self.unsafe_state)
        result = engine.check_safety()
        self.assertFalse(result.is_safe)
        self.assertEqual(len(result.safe_sequence), 0)

    def test_all_safe_sequences(self):
        engine = BankerEngine(self.safe_state)
        all_seqs = engine.find_all_safe_sequences()
        self.assertGreater(len(all_seqs), 0)
        # Every found sequence must have length 5 with unique processes
        for seq in all_seqs:
            self.assertEqual(len(seq), 5)
            self.assertEqual(len(set(seq)), 5)

    def test_single_resource_scenario(self):
        # 1. Unsafe state when Available = 2 (min need is 3)
        state_unsafe = BankerState(
            num_processes=3,
            num_resources=1,
            available=[2],
            max_matrix=[[10], [5], [7]],
            allocation_matrix=[[5], [2], [3]],
        )
        engine_unsafe = BankerEngine(state_unsafe)
        res_unsafe = engine_unsafe.check_safety()
        self.assertFalse(res_unsafe.is_safe)

        # 2. Safe state when Available = 3 (P1 need is 3 <= 3)
        state_safe = BankerState(
            num_processes=3,
            num_resources=1,
            available=[3],
            max_matrix=[[10], [5], [7]],
            allocation_matrix=[[5], [2], [3]],
        )
        engine_safe = BankerEngine(state_safe)
        res_safe = engine_safe.check_safety()
        self.assertTrue(res_safe.is_safe)
        self.assertEqual(res_safe.safe_sequence[0], "P1")


if __name__ == "__main__":
    unittest.main()
