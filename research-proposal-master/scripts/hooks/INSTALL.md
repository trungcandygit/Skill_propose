# Enforcement hooks (bundled copy)

These two hooks make the loading contract binding. The live copies are in `~/.claude/hooks/`; the files here are the reference copies that travel with the skill.

- `skill_gate.py mark` (PostToolUse, matcher `Skill|Read`) records, per session and per agent, which skills were invoked and which cards were read in full.
- `skill_gate.py check` (PreToolUse, matcher `Write|Edit|NotebookEdit|Agent|Artifact`) denies the call until the required skills are invoked and `references/cards/core.md` plus one role card are read in full (no offset/limit). It applies under any path containing `NCKH`, and in any project once `Skill("research-proposal-master")` has been invoked. The deny message names the missing files.
- `force_academic_skills.py` (UserPromptSubmit) reminds every prompt to load the skills and cards.

Install on a new machine: copy both files to `~/.claude/hooks/` and add to `~/.claude/settings.json`:

```json
"hooks": {
  "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/force_academic_skills.py", "timeout": 10}]}],
  "PostToolUse": [{"matcher": "Skill|Read", "hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/skill_gate.py mark", "timeout": 5}]}],
  "PreToolUse": [{"matcher": "Write|Edit|NotebookEdit|Agent|Artifact", "hooks": [{"type": "command", "command": "python3 ~/.claude/hooks/skill_gate.py check", "timeout": 5}]}]
}
```

Why hooks and not only instructions: an instruction can be skipped when context runs long; a hook cannot. When you change the live hooks, copy them back here.
