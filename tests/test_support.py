import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from analyze_support import validate,safe_rate

class SupportAnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.agents=pd.DataFrame([{"agent_id":"A001","agent_name":"Test Agent","team":"Tier 1","region":"Europe"}])
        self.tickets=pd.DataFrame([
          {"ticket_id":"T000001","created_at":"2025-01-01","status":"Closed","priority":"Normal","category":"Billing","channel":"Email","agent_id":"A001","response_hours":2.0,"resolution_hours":10.0,"closed_at":"2025-01-02"},
          {"ticket_id":"T000002","created_at":"2025-01-02","status":"Open","priority":"High","category":"Technical","channel":"Chat","agent_id":"A001","response_hours":1.0,"resolution_hours":float("nan"),"closed_at":float("nan")}])
    def test_valid_data_has_no_errors(self): self.assertEqual(validate(self.tickets,self.agents),[])
    def test_duplicate_ticket_ids_fail(self):
        self.assertIn("ticket_id must be unique",validate(pd.concat([self.tickets,self.tickets.iloc[[0]]],ignore_index=True),self.agents))
    def test_unknown_agent_fails(self):
        bad=self.tickets.copy(); bad.loc[0,"agent_id"]="A999"
        self.assertIn("ticket agent_id must exist in agents",validate(bad,self.agents))
    def test_safe_rate_zero_denominator(self): self.assertIsNone(safe_rate(0,0))
    def test_safe_rate_value(self): self.assertEqual(safe_rate(3,4),.75)
if __name__=="__main__": unittest.main()
