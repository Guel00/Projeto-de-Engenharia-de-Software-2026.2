import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).parents[1]/"services"/"game"/"app"/"challenges.py"; s=importlib.util.spec_from_file_location("challenges",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class ChallengeCatalogTest(unittest.TestCase):
    def test_every_challenge_has_three_options(self):
        for i in m.CHALLENGES:self.assertEqual(len(i["options"]),3)
    def test_best_option_is_valid(self):
        for i in m.CHALLENGES:self.assertIn(i["best_option"],{o["id"] for o in i["options"]})
    def test_non_negative_points(self):
        for i in m.CHALLENGES:self.assertTrue(all(o["points"]>=0 for o in i["options"]))
if __name__=="__main__":unittest.main()
