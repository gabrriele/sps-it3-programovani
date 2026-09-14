import unittest

def je_sude(n):
    return n % 2 == 0

def deleni(a, b):
    if b == 0:
        raise ValueError("Nelze dělit nulou!")
    return a / b

class TestRuzneAsserty(unittest.TestCase):
    def test_assertEqual(self):
        self.assertEqual(2 + 2, 4)

    def test_assertNotEqual(self):
        self.assertNotEqual(2 + 2, 5)

    def test_assertTrue(self):
        self.assertTrue(je_sude(4))

    def test_assertFalse(self):
        self.assertFalse(je_sude(3))

    def test_assertIn(self):
        self.assertIn("a", "ahoj")

    def test_assertRaises(self):
        with self.assertRaises(ValueError):
            deleni(10, 0)

if __name__ == '__main__':
    unittest.main()