#!/usr/bin/env python3
import json
from pathlib import Path
def validate(path):
    p = Path(path)
    return {"plugin_json": (p/".claude-plugin/plugin.json").exists(), "agents": (p/"agents").is_dir(), "skills": (p/"skills").is_dir()}
if __name__ == "__main__":
    import sys; print(json.dumps(validate(sys.argv[1] if len(sys.argv)>1 else "."), indent=2))
