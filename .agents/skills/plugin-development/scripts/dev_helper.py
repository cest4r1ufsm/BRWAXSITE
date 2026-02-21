#!/usr/bin/env python3
import json
from pathlib import Path
def create_skill_scaffold(skill_name, path="."):
    p = Path(path) / "skills" / skill_name
    for d in ["assets", "scripts", "references"]: (p / d).mkdir(parents=True, exist_ok=True)
    (p / "SKILL.md").write_text(f"---\nname: {skill_name}\n---\n# {skill_name}")
    return {"created": str(p)}
if __name__ == "__main__":
    import sys; print(json.dumps(create_skill_scaffold(sys.argv[1] if len(sys.argv)>1 else "new-skill"), indent=2))
