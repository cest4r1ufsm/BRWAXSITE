#!/usr/bin/env python3
import json, re
from pathlib import Path
def check_design(path):
    p = Path(path)
    agents = list((p/"agents").glob("*.md")) if (p/"agents").exists() else []
    skills = list((p/"skills").iterdir()) if (p/"skills").exists() else []
    return {"agents": len(agents), "skills": len(skills), "balanced": len(agents) == len(skills)}
if __name__ == "__main__":
    import sys; print(json.dumps(check_design(sys.argv[1] if len(sys.argv)>1 else "."), indent=2))
