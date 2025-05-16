
import unittest
from server import GuessingGameServer

class FixedRandom:
    def randint(self, a, b):
        return 42  # Fixed number for deterministic test

class TestGuessingGameServer(unittest.TestCase):

    def setUp(self):
        self.server = GuessingGameServer(rng=FixedRandom())
        self.server.secret_number = 42 
    def tearDown(self):
        self.server.stop()


    def test_too_low(self):
        response, _ = self.server.evaluate_guess(30, 1)
        self.assertEqual(response, "Too low!")

    def test_too_high(self):
        response, _ = self.server.evaluate_guess(90, 1)
        self.assertEqual(response, "Too high!")

    def test_correct_very_good(self):
        response, done = self.server.evaluate_guess(42, 3)
        self.assertIn("Correct! You win!: 3 guesses = very good", response)
        self.assertTrue(done)

    def test_correct_good(self):
        response, done = self.server.evaluate_guess(42, 7)
        self.assertIn("Correct! You win!: 7 guesses = good", response)

    def test_correct_fair(self):
        response, done = self.server.evaluate_guess(42, 15)
        self.assertIn("Correct! You win!: 15 guesses = fair", response)

if __name__ == '__main__':
    unittest.main()
