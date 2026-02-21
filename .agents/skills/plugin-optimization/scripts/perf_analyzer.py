#!/usr/bin/env python3
import json
from pathlib import Path
def analyze(path):
    p = Path(path)
    files = list(p.rglob("*.md"))
    total_size = sum(f.stat().st_size for f in files)
    return {"md_files": len(files), "total_bytes": total_size, "avg_size": total_size // len(files) if files else 0}
if __name__ == "__main__":
    import sys; print(json.dumps(analyze(sys.argv[1] if len(sys.argv)>1 else "."), indent=2))
