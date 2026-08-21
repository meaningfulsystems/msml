"""Locked Cursor / Claude skill slugs, AGENTS.md, and the new-project template.

SysML2d uses the same four skill directory names so both repos can share
one adoption story. This test fails if a rename or a second parallel
playbook appears.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from msml import validate
from msml.render import render
from msml.spec import spec_path


REPO = Path(__file__).resolve().parents[1]

REQUIRED_SKILLS = (
    "bootstrap-project",
    "author-model",
    "compose-views",
    "vision-review",
)

TWELVE_VIEW_TYPES = (
    "bdd",
    "ibd",
    "activity",
    "sequence",
    "state_machine",
    "use_case",
    "requirement",
    "parametric",
    "package",
    "requirement_table",
    "allocation_table",
    "allocation_matrix",
)


class AdoptionPackTests(unittest.TestCase):
    def test_agents_md_exists_and_names_the_loop(self) -> None:
        text = (REPO / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("skills/bootstrap-project/SKILL.md", text)
        self.assertIn("skills/author-model/SKILL.md", text)
        self.assertIn("skills/compose-views/SKILL.md", text)
        self.assertIn("skills/vision-review/SKILL.md", text)
        self.assertIn("https://github.com/meaningfulsystems/sysml2d", text)
        self.assertIn("templates/new-project/", text)
        self.assertIn("msml-validate", text)
        self.assertIn("msml-render", text)

    def test_four_skill_files_exist(self) -> None:
        for slug in REQUIRED_SKILLS:
            path = REPO / "skills" / slug / "SKILL.md"
            self.assertTrue(path.is_file(), f"missing {path}")
            body = path.read_text(encoding="utf-8")
            self.assertIn(f"name: {slug}", body)

    def test_compose_views_covers_all_twelve_types(self) -> None:
        body = (REPO / "skills/compose-views/SKILL.md").read_text(encoding="utf-8")
        for view_type in TWELVE_VIEW_TYPES:
            self.assertIn(f"`{view_type}`", body)
        self.assertIn("msml-validate", body)
        self.assertIn("msml-render", body)
        self.assertIn("msml-render-all", body)

    def test_vision_review_states_hard_rule(self) -> None:
        body = (REPO / "skills/vision-review/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("never pass over boxes", body)
        self.assertIn("overlapping labels", body.lower())
        self.assertIn("leftover canvas", body.lower())

    def test_starter_template_exists(self) -> None:
        self.assertTrue((REPO / "templates/new-project").is_dir())

    def test_no_second_skills_tree(self) -> None:
        extras = [
            path
            for path in (REPO / "ai-collab").rglob("SKILL.md")
            if path.is_file()
        ]
        self.assertEqual(
            extras,
            [],
            "ai-collab/ must not grow a second SKILL.md tree; fold into skills/",
        )

    def test_readme_points_at_start_your_own_system(self) -> None:
        text = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn("Start your own system", text)
        self.assertIn("AGENTS.md", text)
        self.assertIn("skills/bootstrap-project/SKILL.md", text)
        self.assertIn("templates/new-project/", text)
        self.assertIn("https://github.com/meaningfulsystems/sysml2d", text)

    def test_template_validates_and_renders(self) -> None:
        model = REPO / "templates/new-project/architecture/system-model.msml"
        view = REPO / "templates/new-project/architecture/system-context.msmd"
        model_report = validate(model, strict=True)
        view_report = validate(view, strict=True)
        self.assertEqual(model_report.errors, 0)
        self.assertEqual(view_report.errors, 0)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "system-context.png"
            render(view, out)
            self.assertTrue(out.is_file())
            self.assertGreater(out.stat().st_size, 1000)

    def test_template_is_not_a_copy_of_electric_bike(self) -> None:
        model = (
            REPO / "templates/new-project/architecture/system-model.msml"
        ).read_text(encoding="utf-8")
        self.assertNotIn("ElectricBike", model)
        self.assertIn("ExampleSystem", model)

    def test_packaged_spec_is_available(self) -> None:
        path = spec_path()
        self.assertTrue(path.is_file())
        self.assertGreater(path.stat().st_size, 100)
