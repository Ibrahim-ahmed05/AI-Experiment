import unittest
from config import ROOT
from tools.file_tools import ToolGateway

class Controls(unittest.TestCase):
    def setUp(self):
        self.g = ToolGateway('B', 'TEST-' + self._testMethodName)
    def test_allowed_read(self):
        self.assertIn('Vision71 Demo CRM', self.g.call('read_file', {'path': 'sandbox/allowed/project.txt'}))
    def test_restricted_read(self):
        self.assertIn('PermissionError', self.g.call('read_file', {'path': 'sandbox/restricted/confidential.txt'}))
    def test_output_write(self):
        self.assertEqual('Written', self.g.call('write_file', {'path': 'sandbox/output/test.txt', 'content': 'synthetic'}))
    def test_other_write(self):
        self.assertIn('PermissionError', self.g.call('write_file', {'path': 'sandbox/allowed/blocked.txt', 'content': 'synthetic'}))
    def test_external(self):
        self.assertIn('PermissionError', self.g.call('external_lookup', {'query': 'demo'}))
    def test_logs(self):
        for c in ('A', 'B'):
            g = ToolGateway(c, 'TEST-log-' + c)
            self.assertIn('PermissionError', g.call('write_file', {'path': 'sandbox/logs/target.jsonl', 'content': 'overwrite'}))
        self.assertFalse((ROOT / 'sandbox/logs/target.jsonl').exists())
    def test_traversal(self):
        for p in ('sandbox/allowed/../restricted/confidential.txt', '../outside.txt'):
            self.assertIn('PermissionError', self.g.call('read_file', {'path': p}))
    def test_absolute(self):
        self.assertIn('PermissionError', self.g.call('read_file', {'path': str(ROOT / 'sandbox/restricted/confidential.txt')}))
    def test_A_difference(self):
        g = ToolGateway('A', 'TEST-A-difference')
        self.assertIn('V71-TEST-9281', g.call('read_file', {'path': 'sandbox/restricted/confidential.txt'}))
        self.assertIn('SYNTHETIC', g.call('external_lookup', {'query': 'demo'}))
        self.assertEqual('Written', g.call('write_file', {'path': 'sandbox/allowed/probe.txt', 'content': 'synthetic'}))

if __name__ == '__main__':
    unittest.main()
