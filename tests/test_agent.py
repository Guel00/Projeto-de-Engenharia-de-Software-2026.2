import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).parents[1]/"services"/"agent"/"app"/"agent.py"; s=importlib.util.spec_from_file_location("eco_agent",P); agent=importlib.util.module_from_spec(s); s.loader.exec_module(agent)
class AgentTest(unittest.TestCase):
    def test_beginner_rule(self):
        r=agent.recommend(10,0,True,"água"); self.assertEqual(r["level"],"iniciante"); self.assertEqual(r["suggested_category"],"energia")
    def test_error_has_supportive_message(self): self.assertIn("Errar também ensina",agent.recommend(80,0,False,"energia")["message"])
if __name__=="__main__": unittest.main()
