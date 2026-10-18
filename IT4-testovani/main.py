import unittest

def text_na_velka(text):
    if isinstance(text, str):
        return text.upper()
    else:
        raise TypeError


class TestObsahujeJenPismena(unittest.TestCase):
    def test_mala_na_velka(self):
        self.assertEqual(text_na_velka("abc"),"ABC")

    def test_uz_velka(self):
        self.assertEqual(text_na_velka("NEZKLAMU VÁS!"), "NEZKLAMU VÁS!")

    def test_smiseny_text(self):
        self.assertEqual(text_na_velka("čAu liDi"), "ČAU LIDI")

    def test_cislo(self):
        with self.assertRaises(TypeError):
            text_na_velka(99)



if __name__ == '__main__':
    unittest.main()