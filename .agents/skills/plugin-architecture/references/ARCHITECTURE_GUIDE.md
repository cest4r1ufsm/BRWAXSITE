# Plugin Architecture Guide

## Structure
```
plugin/
├── .claude-plugin/
│   └── plugin.json
├── agents/
├── skills/
├── commands/
└── hooks/
```

## SASMP v1.3.0
- Agents: name, model, tools, sasmp_version, eqhm_enabled
- Skills: name, bonded_agent, bond_type
