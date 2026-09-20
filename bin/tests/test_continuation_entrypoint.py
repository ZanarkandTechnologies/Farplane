"""Global continuation hooks must not depend on the caller's Doppler setup."""
import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('continuation_gate', ROOT / 'hooks/continuation_gate.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class EntrypointTests(unittest.TestCase):
    def test_credentials_resolve_from_owner_not_caller(self):
        with patch.object(gate, 'load_runtime_env', return_value={}), patch.object(gate.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '{"decision":"block","reason":"continue"}', '')) as run:
            self.assertEqual(gate.run_gate({'hook_event_name':'Stop'})['decision'], 'block')
            self.assertEqual(run.call_args.kwargs['cwd'], ROOT)
            self.assertEqual(run.call_args.kwargs['timeout'], 4)
            self.assertTrue(run.call_args.kwargs['capture_output'])

    def test_missing_doppler_and_errors_allow_stop(self):
        for failure in (FileNotFoundError(), subprocess.TimeoutExpired('doppler', 4)):
            with self.subTest(failure=type(failure).__name__), patch.object(gate, 'load_runtime_env', return_value={}), patch.object(gate.subprocess, 'run', side_effect=failure):
                self.assertIsNone(gate.run_gate({}))
        with patch.object(gate, 'load_runtime_env', return_value={}), patch.object(gate.subprocess, 'run', return_value=subprocess.CompletedProcess([], 2, '', 'doppler_not_configured')):
            self.assertIsNone(gate.run_gate({}))

    def test_child_never_recurses_without_credentials(self):
        with patch.object(gate, 'load_runtime_env', return_value={}), patch.object(gate.subprocess, 'run') as run, patch.object(gate, 'evaluate_stop', return_value=None) as evaluate:
            self.assertIsNone(gate.run_gate({}, credential_child=True))
            run.assert_not_called()
            evaluate.assert_called_once()

    def test_existing_credentials_skip_wrapper(self):
        with patch.object(gate, 'load_runtime_env', return_value={'OPENROUTER_API_KEY':'synthetic'}), patch.object(gate.subprocess, 'run') as run, patch.object(gate, 'evaluate_stop', return_value=None):
            self.assertIsNone(gate.run_gate({}))
            run.assert_not_called()

if __name__ == '__main__':
    unittest.main()
