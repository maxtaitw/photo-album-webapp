# Working style

- Always make a plan before editing files.
- Never implement a large feature in one step.
- Prefer incremental changes that I can review and understand.
- Explain why each proposed change is needed.
- After edits, tell me what changed and what I should learn from it.
- Ask before adding dependencies.
- Prefer modifying existing files over creating many new files unless structure really requires it.
- Run tests or linters after each meaningful change when possible.

# Commit messages

Use commit messages in this format:

```text
<type>: <short imperative summary>
```

Allowed types:

- build
- chore
- docs
- feat
- fix
- refactor
- test

Rules:

- One commit = one clear purpose.
- Keep each commit focused and reviewable.
- No vague messages like "update", "changes", or "fix stuff".
- Match the message to the actual scope of the diff.
