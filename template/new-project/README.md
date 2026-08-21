# New MSML project

Copy this folder into your repository, then rename the system.

```bash
mkdir -p architecture
cp template/new-project/architecture/system-model.msml architecture/
cp template/new-project/architecture/system-context.msmd architecture/
msml-spec --copy architecture/
msml-validate architecture/system-context.msmd --strict
msml-render architecture/system-context.msmd
```

Next: follow [AGENTS.md](../../AGENTS.md) — author-model, compose-views (render), vision-review.

This is MSML (`.msml` / `.msmd` / PNG), not SysML2d. Pick one toolchain per project.
