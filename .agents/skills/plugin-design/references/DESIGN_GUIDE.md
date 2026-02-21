# Plugin Design Guide

## Agent-Skill Bonding
- Each agent should have PRIMARY_BOND skill
- Skills declare bonded_agent in frontmatter
- No orphan skills or ghost agents

## Golden Format
```
skills/skill-name/
├── SKILL.md
├── assets/    # YAML configs
├── scripts/   # Python utilities
└── references/ # GUIDE.md docs
```
