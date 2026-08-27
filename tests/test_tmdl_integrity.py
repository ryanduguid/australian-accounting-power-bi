"""
test_tmdl_integrity.py - Validates TMDL definitions, star schema relationships, and measure hygiene.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_NAME = "australian-accounting-power-bi"
PROJECT_FILE = BASE_DIR / f"{PROJECT_NAME}.pbip"
REPORT_DIR = BASE_DIR / f"{PROJECT_NAME}.Report"
SEMANTIC_MODEL_DIR = BASE_DIR / f"{PROJECT_NAME}.SemanticModel"
TMDL_DIR = SEMANTIC_MODEL_DIR / "definition"
TMDL_TABLES_DIR = TMDL_DIR / "tables"
RELATIONSHIPS_FILE = TMDL_DIR / "relationships.tmdl"
DATABASE_FILE = TMDL_DIR / "database.tmdl"


class TestTmdlIntegrity(unittest.TestCase):
    def test_project_path_graph_uses_one_canonical_identifier(self) -> None:
        project = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))
        report = json.loads((REPORT_DIR / "definition.pbir").read_text(encoding="utf-8"))
        database = DATABASE_FILE.read_text(encoding="utf-8")

        self.assertEqual(
            project["artifacts"][0]["report"]["path"],
            f"{PROJECT_NAME}.Report",
        )
        self.assertEqual(
            report["datasetReference"]["byPath"]["path"],
            f"../{PROJECT_NAME}.SemanticModel",
        )
        self.assertIn(f"database '{PROJECT_NAME}'", database)

    def test_tables_directory_exists_and_populated(self) -> None:
        self.assertTrue(TMDL_TABLES_DIR.is_dir(), "TMDL tables directory must exist")
        tmdl_files = list(TMDL_TABLES_DIR.glob("*.tmdl"))
        self.assertGreaterEqual(len(tmdl_files), 8, "Expected at least 8 TMDL table definitions")

    def test_relationships_defined_and_valid(self) -> None:
        self.assertTrue(RELATIONSHIPS_FILE.is_file(), "relationships.tmdl must exist")
        content = RELATIONSHIPS_FILE.read_text(encoding="utf-8")

        rel_blocks = re.findall(
            r"relationship\s+'([^']+)'\s+fromColumn:\s+([\w\.]+)\s+toColumn:\s+([\w\.]+)",
            content,
        )
        self.assertGreaterEqual(len(rel_blocks), 5, "Expected at least 5 star schema relationships")

        for name, from_col, to_col in rel_blocks:
            self.assertIn(".", from_col, f"Relationship {name} fromColumn must include table name")
            self.assertIn(".", to_col, f"Relationship {name} toColumn must include table name")

    def test_all_measures_have_supported_descriptions_and_numeric_formats(self) -> None:
        """Require descriptions for every measure and formats for non-text measures."""
        tmdl_files = list(TMDL_TABLES_DIR.glob("*.tmdl"))
        measure_count = 0
        unformatted_measures: list[str] = []

        for tmdl_file in tmdl_files:
            lines = tmdl_file.read_text(encoding="utf-8").splitlines()
            object_starts = [
                index
                for index, line in enumerate(lines)
                if re.match(
                    r"^\t(?:measure|column|partition|hierarchy|calculationGroup|annotation)\b",
                    line,
                )
            ]

            for index, line in enumerate(lines):
                if not line.startswith("\tmeasure "):
                    continue

                measure_name = line.removeprefix("\tmeasure ").split(" =", 1)[0].strip("'")
                measure_count += 1
                next_object = next(
                    (object_index for object_index in object_starts if object_index > index),
                    len(lines),
                )
                block = "\n".join(lines[index:next_object])

                if "formatString:" not in block and "formatStringDefinition" not in block:
                    unformatted_measures.append(f"{tmdl_file.name}:[{measure_name}]")
                self.assertTrue(
                    index > 0 and lines[index - 1].startswith("\t/// "),
                    f"Measure [{measure_name}] in {tmdl_file.name} is missing a supported description",
                )

        self.assertEqual(measure_count, 43, "Expected exactly 43 explicit DAX measures across model")
        self.assertEqual(
            unformatted_measures,
            ["Fact_ATOBenchmark.tmdl:[ATO Compliance Risk Profile]"],
            "Only the text-valued risk-profile measure may omit a numeric format string",
        )

    def test_calculation_groups_have_precedence_and_ordinals(self) -> None:
        """Calculation groups must declare explicit precedence and ordinals on calculation items."""
        cg_files = [f for f in TMDL_TABLES_DIR.glob("*.tmdl") if "CalcGroup" in f.name]
        self.assertGreaterEqual(len(cg_files), 2, "Expected at least 2 calculation groups")

        for cg_file in cg_files:
            content = cg_file.read_text(encoding="utf-8")
            self.assertIn("calculationGroup", content, f"{cg_file.name} must declare calculationGroup block")
            self.assertIn("precedence:", content, f"{cg_file.name} must specify precedence")
            self.assertIn("ordinal:", content, f"{cg_file.name} calculation items must have ordinals")


if __name__ == "__main__":
    unittest.main()
