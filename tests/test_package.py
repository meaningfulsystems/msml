import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures"

from msml import spec_path, validate, validate_all
from msml.render import render
from msml.render_all import render_all


class PackageApiTests(unittest.TestCase):
    def validate_with_output(self, path: Path, **kwargs):
        output = StringIO()
        with redirect_stdout(output):
            report = validate(path, **kwargs)
        return report, output.getvalue()

    def test_spec_is_packaged(self):
        path = spec_path()
        self.assertTrue(path.exists())
        self.assertIn("MSML v1.0 Specification", path.read_text())

    def test_packaged_spec_matches_root_spec(self):
        self.assertEqual(
            (ROOT / "msml-specification.md").read_bytes(),
            spec_path().read_bytes(),
        )

    def test_validate_example_diagram(self):
        report = validate(ROOT / "projects/appliances/toaster/toaster-bdd.msmd", strict=True)
        self.assertEqual(report.errors, 0)

    def test_validate_hos_diagrams(self):
        report = validate_all(ROOT / "projects/humanity-optimization", strict=True)
        self.assertEqual(report.errors, 0)

    def test_validate_all_projects(self):
        report = validate_all(ROOT / "projects", strict=True)
        self.assertEqual(report.errors, 0)

    def test_valid_import_chain(self):
        report, output = self.validate_with_output(FIXTURES / "import-chain.msmd", strict=True)
        self.assertEqual(report.errors, 0, output)

    def test_missing_model_ref_reports_schema_005(self):
        report, output = self.validate_with_output(FIXTURES / "missing-model-ref.msmd")
        self.assertGreater(report.errors, 0)
        self.assertIn("MSML-SCHEMA-005", output)

    def test_missing_relationship_ref_reports_schema_006(self):
        report, output = self.validate_with_output(FIXTURES / "missing-relationship-ref.msmd")
        self.assertGreater(report.errors, 0)
        self.assertIn("MSML-SCHEMA-006", output)

    def test_singular_model_file_reports_schema_009(self):
        report, output = self.validate_with_output(FIXTURES / "singular-model-file.msmd")
        self.assertGreater(report.errors, 0)
        self.assertIn("MSML-SCHEMA-009", output)

    def test_duplicate_definition_reports_schema_004(self):
        report, output = self.validate_with_output(FIXTURES / "duplicate-definition.msml")
        self.assertGreater(report.errors, 0)
        self.assertIn("MSML-SCHEMA-004", output)

    def test_lint_orphan_reports_warnings(self):
        report, output = self.validate_with_output(FIXTURES / "lint-orphan.msmd", lint=True)
        self.assertEqual(report.errors, 0, output)
        self.assertGreater(report.warnings, 0)
        self.assertIn("MSML-LINT-004", output)
        self.assertIn("MSML-LINT-005", output)

    def test_render_rejects_model_file(self):
        with self.assertRaises(ValueError):
            render(ROOT / "projects/appliances/toaster/toaster-model.msml")

    def test_render_all_examples(self):
        self.assertEqual(render_all(ROOT / "projects/appliances/toaster"), 0)

    def test_render_all_projects(self):
        self.assertEqual(render_all(ROOT / "projects"), 0)
        diagrams = sorted((ROOT / "projects").rglob("*.msmd"))
        self.assertGreaterEqual(len(diagrams), 19)
        for diagram in diagrams:
            png = diagram.with_suffix(".png")
            self.assertTrue(png.exists(), f"missing PNG for {diagram.name}")
            self.assertGreater(png.stat().st_size, 1000, f"empty PNG for {diagram.name}")

    def test_toaster_tabular_views_validate(self):
        for name in ("toaster-reqt.msmd", "toaster-alloc.msmd", "toaster-amx.msmd"):
            report = validate(ROOT / "projects/appliances/toaster" / name, strict=True)
            self.assertEqual(report.errors, 0, name)

    def test_spec_documents_tabular_views(self):
        text = (ROOT / "msml-specification.md").read_text()
        self.assertIn("requirement_table", text)
        self.assertIn("allocation_table", text)
        self.assertIn("allocation_matrix", text)
        self.assertIn("`allocate`", text)

    def test_architecture_design_notes(self):
        folders = [
            ROOT / "projects/e-bike",
            ROOT / "projects/apollo",
            ROOT / "projects/appliances/toaster",
            ROOT / "projects/appliances/blender",
            ROOT / "projects/humanity-optimization",
        ]
        required = (
            "## 1. Purpose / context",
            "## 2. System boundary and actors",
            "## 3. Requirements",
            "## 4. Structure and interfaces",
            "## 5. States and modes",
            "## 6. Allocations (req → part)",
            "## 7. Sourced numbers",
            "## 8. Open risks / TBD",
            "## 9. Views in this folder",
        )
        for folder in folders:
            path = folder / "architecture-summary.md"
            self.assertTrue(path.exists(), path)
            text = path.read_text(encoding="utf-8")
            for heading in required:
                self.assertIn(heading, text, f"{path.name} missing {heading}")
            lowered = text.lower()
            self.assertNotIn("cloud agent", lowered)
            self.assertNotIn("mrs.", lowered)
            self.assertNotIn("mr.", lowered)
        ebike = (ROOT / "projects/e-bike/architecture-summary.md").read_text(encoding="utf-8")
        self.assertIn("continuous", ebike)
        self.assertIn("250 W", ebike)
        self.assertIn("40 N·m", ebike)
        self.assertIn("lockBike", ebike)
        apollo = (ROOT / "projects/apollo/architecture-summary.md").read_text(encoding="utf-8")
        self.assertIn("official CSM lunar Δv", apollo)
        self.assertIn("CSM-107 SPS loaded", apollo)
        self.assertIn("20,500", apollo)
        self.assertIn("21,500", apollo)
        self.assertIn("9,870", apollo)
        self.assertIn("10,500", apollo)
        self.assertIn("apollo-stm.png", apollo)


if __name__ == "__main__":
    unittest.main()
