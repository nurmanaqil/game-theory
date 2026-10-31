import tempfile
import unittest
from pathlib import Path

from checkpoint_integrity import checkpoint_context, record_checkpoint, verify_checkpoint


class CheckpointIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = self.root / 'train.csv'
        self.data.write_text('x,y\n1,0\n')
        self.model = self.root / 'model.joblib'
        self.model.write_bytes(b'synthetic checkpoint; never deserialized')
        self.context = checkpoint_context([self.data], {'depth': 3, 'seed': 42}, {'python': 'test'})

    def test_unchanged_checkpoint_is_accepted(self):
        record_checkpoint(self.model, self.context)
        verify_checkpoint(self.model, self.context)

    def test_missing_metadata_is_rejected(self):
        with self.assertRaises(ValueError):
            verify_checkpoint(self.model, self.context)

    def test_changed_training_data_is_rejected(self):
        record_checkpoint(self.model, self.context)
        self.data.write_text('x,y\n2,0\n')
        changed = checkpoint_context([self.data], {'depth': 3, 'seed': 42}, {'python': 'test'})
        with self.assertRaises(ValueError):
            verify_checkpoint(self.model, changed)

    def test_changed_configuration_is_rejected(self):
        record_checkpoint(self.model, self.context)
        changed = checkpoint_context([self.data], {'depth': 4, 'seed': 42}, {'python': 'test'})
        with self.assertRaises(ValueError):
            verify_checkpoint(self.model, changed)

    def test_changed_runtime_is_rejected(self):
        record_checkpoint(self.model, self.context)
        changed = checkpoint_context([self.data], {'depth': 3, 'seed': 42}, {'python': 'other'})
        with self.assertRaises(ValueError):
            verify_checkpoint(self.model, changed)

    def test_changed_checkpoint_is_rejected(self):
        record_checkpoint(self.model, self.context)
        self.model.write_bytes(b'changed')
        with self.assertRaises(ValueError):
            verify_checkpoint(self.model, self.context)


if __name__ == '__main__':
    unittest.main()
