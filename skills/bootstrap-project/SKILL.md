---
name: bootstrap-project
description: Start a new MSML project from the template. Use when the user wants a new system model, a first architecture folder, or “start your own system.”
---

# Bootstrap an MSML project

Copy the starter, copy the spec, write the first model and one view, then validate and render. Do not invent a second file format.

## When to use

- A user says “start a new system,” “new MSML project,” or “scaffold architecture.”
- You are beginning work in an empty folder that should become an MSML project.

Do not use this skill to edit an existing `.msml` (author-model) or to add more views (compose-views).

## Steps

1. **Install MSML** in the user’s project if the CLI is missing:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install git+https://github.com/meaningfulsystems/msml.git
   ```

2. **Copy the template.** The locked path is `templates/new-project/`.

   ```bash
   mkdir -p architecture
   cp templates/new-project/architecture/system-model.msml architecture/
   cp templates/new-project/architecture/system-context.msmd architecture/
   ```

   If you are already inside this repository, copy from the repo root. If the user is in another repo, copy those two files (or the whole `templates/new-project/` tree) into their project.

3. **Copy the specification** next to the model so humans and agents share the rules:

   ```bash
   msml-spec --copy architecture/
   ```

4. **Rename the system.** Edit `architecture/system-model.msml`:
   - Change `namespace`, root block `id` / `name`, and the context block to the user’s system.
   - Keep actor / environment / system as three context members. Do not invent extra context actors on day one.

5. **Point the view at the model.** `architecture/system-context.msmd` already lists `"model_files": ["system-model.msml"]`. Update `model_ref`, `subject_ref`, and display names to match the renamed ids.

6. **Validate and render:**

   ```bash
   msml-validate architecture/system-context.msmd --strict
   msml-render architecture/system-context.msmd
   ```

   The PNG is written next to the `.msmd`.

7. **Hand off.** Next skill is [author-model](../author-model/SKILL.md) to grow the model, then [compose-views](../compose-views/SKILL.md) for more diagrams, then [vision-review](../vision-review/SKILL.md) before commit.

## Template contents

| Path | Role |
| --- | --- |
| `templates/new-project/README.md` | What the user copies and runs |
| `templates/new-project/architecture/system-model.msml` | Stub system, operator, environment, context |
| `templates/new-project/architecture/system-context.msmd` | One context IBD |

## Pitfalls

- Do not start from toaster or e-bike by copying the whole example. Those are references; the template is the starter.
- Do not create `.sysml` or SysML2d intent JSON here. That is the sibling repo.
- ElectricBike qualified names in `projects/e-bike/` are frozen. A *new* project gets *new* ids.
- `ibd` views need `diagram.subject_ref` pointing at a **block**.
