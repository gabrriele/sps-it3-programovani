import unittest


def je_sude(n):
    return n % 2 == 0


# TODO: Úloha 1
class TestJeSude(unittest.TestCase):
    def test_kladne_sude(self):
        self.assertEqual(je_sude(4), True)

    def test_kladne_liche(self):
        self.assertEqual(je_sude(3), True)

    def test_nula(self):
        self.assertEqual(je_sude(0), True)

    def test_zaporne_liche(self):
         self.assertEqual(je_sude(-3), False)



if __name__ == '__main__':
    unittest.main()