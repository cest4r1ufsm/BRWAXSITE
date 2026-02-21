#!/usr/bin/env python3
import json, re
from pathlib import Path
def test_plugin(path):
    p = Path(path)
    results = {"structure": (p/".claude-plugin/plugin.json").exists(), "agents": (p/"agents").is_dir(), "skills": (p/"skills").is_dir()}
    results["passed"] = all(results.values())
    return results
if __name__ == "__main__":
    import sys; print(json.dumps(test_plugin(sys.argv[1] if len(sys.argv)>1 else "."), indent=2))
