"""Validate checkpoint provenance without deserializing model files."""
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def checkpoint_context(inputs, configuration, versions):
    # Names are relative to the common input directory, so moving a project
    # does not invalidate an otherwise identical experiment.
    paths = [Path(p).resolve() for p in inputs]
    import os
    root = Path(os.path.commonpath([str(p.parent) for p in paths]))
    return {
        'inputs': {p.relative_to(root).as_posix(): digest(p) for p in paths},
        'configuration': configuration,
        'versions': versions,
    }


def record_checkpoint(path, context):
    path = Path(path)
    metadata = {'context': context, 'sha256': digest(path)}
    sidecar = path.with_name(path.name + '.provenance.json')
    temporary = sidecar.with_name(sidecar.name + '.partial')
    temporary.write_text(json.dumps(metadata, sort_keys=True, indent=2), encoding='utf-8')
    temporary.replace(sidecar)


def verify_checkpoint(path, context):
    path = Path(path)
    sidecar = path.with_name(path.name + '.provenance.json')
    if not sidecar.is_file():
        raise ValueError(f'Checkpoint has no provenance: {path}. Use a fresh output directory.')
    metadata = json.loads(sidecar.read_text(encoding='utf-8'))
    if metadata.get('context') != context or metadata.get('sha256') != digest(path):
        raise ValueError(f'Checkpoint provenance mismatch: {path}. Use a fresh output directory.')
