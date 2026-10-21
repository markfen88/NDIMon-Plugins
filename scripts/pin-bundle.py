#!/usr/bin/env python3
"""Record the identity of an explicitly supplied native Tessera runtime bundle."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile

root = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('archive', type=Path)
args = parser.parse_args()
archive = args.archive.resolve(strict=True)
with tarfile.open(archive) as tf:
    members = [m for m in tf.getmembers() if m.isfile() and m.name.endswith('/manifest.json')]
    if len(members) != 1:
        parser.error('one runtime manifest required')
    manifest = json.load(tf.extractfile(members[0]))
if manifest['name'] != 'tessera' or not re.fullmatch('[0-9a-f]{40}', manifest['commit']):
    parser.error('invalid runtime identity')
platform = manifest['os']
if not ((platform['id'], platform['version_id'], manifest['arch']) in
        {('debian', '13', 'amd64'), ('debian', '13', 'arm64'), ('ubuntu', '24.04', 'arm64')}):
    parser.error('unsupported release platform')
entry = {k: manifest[k] for k in ('name', 'version', 'arch', 'commit', 'os')}
entry.update(asset=archive.name, sha256=hashlib.sha256(archive.read_bytes()).hexdigest())
path = root / 'bundles.lock.json'
doc = json.loads(path.read_text()) if path.exists() else {'schema_version': 1, 'bundles': []}
doc['bundles'] = [b for b in doc['bundles'] if (b['os']['id'], b['os']['version_id'], b['arch']) !=
                  (platform['id'], platform['version_id'], entry['arch'])]
doc['bundles'].append(entry)
doc['bundles'].sort(key=lambda b: (b['os']['id'], b['os']['version_id'], b['arch']))
path.write_text(json.dumps(doc, indent=2) + '\n')
print('Pinned', entry['version'], platform['id'], platform['version_id'], entry['arch'])
