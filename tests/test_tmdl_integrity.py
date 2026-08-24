"""
test_tmdl_integrity.py - Validates TMDL definitions, star schema relationships, and measure hygiene.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TMDL_TABLES_DIR = BASE_DIR / "au-financial-analytics-pbip.SemanticModel" / "tables"
RELATIONSHIPS_FILE = BASE_DIR / "au-financial-analytics-pbip.SemanticModel" / "relationships.tmdl"


class TestTmdlIntegrity(unittest.TestCase):
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

    def test_all_measures_have_format_string_and_description(self) -> None:
        """Enforces enterprise BI best practice: every explicit measure must be documented and formatted."""
        tmdl_files = list(TMDL_TABLES_DIR.glob("*.tmdl"))
        measure_count = 0

        for tmdl_file in tmdl_files:
            content = tmdl_file.read_text(encoding="utf-8")
            # Find all measure blocks
            # Pattern matches: measure 'Name' = ... or measure Name = ...
            measure_matches = re.finditer(
                r"\bmeasure\s+(?:'([^']+)'|([\w\s%$\(\)]+))\s*=",
                content,
            )

            for match in measure_matches:
                measure_name = match.group(1) or match.group(2)
                measure_count += 1
                start_pos = match.start()
                # Grab a chunk following the measure definition to inspect attributes
                chunk = content[start_pos : start_pos + 1200]

                has_format_string = "formatString:" in chunk or "formatStringDefinition" in chunk
                has_description = "description:" in chunk

                self.assertTrue(
                    has_format_string,
                    f"Measure [{measure_name}] in {tmdl_file.name} is missing an explicit formatString",
                )
                self.assertTrue(
                    has_description,
                    f"Measure [{measure_name}] in {tmdl_file.name} is missing a description",
                )

        self.assertGreaterEqual(measure_count, 15, "Expected at least 15 explicit DAX measures across model")

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
