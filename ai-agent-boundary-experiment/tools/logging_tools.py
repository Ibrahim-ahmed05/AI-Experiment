import json
from datetime import datetime, timezone
from config import ROOT

def timestamp():
    return datetime.now(timezone.utc).isoformat()

def append(entry):
    path = ROOT / 'sandbox/logs' / (entry['run_id'] + '.jsonl')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n')
