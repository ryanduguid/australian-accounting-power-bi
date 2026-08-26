"""
test_powerquery_m.py - Static syntax and structure checks for Power Query (M) modules.
"""

from __future__ import annotations

import csv
import re
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PQ_DIR = BASE_DIR / "powerquery"
SAMPLES_DIR = BASE_DIR / "samples"


class TestPowerQueryM(unittest.TestCase):
    def test_pq_directory_exists(self) -> None:
        self.assertTrue(PQ_DIR.is_dir(), "powerquery directory must exist")
        pq_files = list(PQ_DIR.glob("*.pq"))
        self.assertGreaterEqual(len(pq_files), 5, "Expected at least 5 Power Query .pq files")

    def test_pq_files_balanced_let_in(self) -> None:
        """Every M script must have balanced let ... in blocks."""
        for pq_file in PQ_DIR.glob("*.pq"):
            content = pq_file.read_text(encoding="utf-8")
            let_count = content.count("let")
            in_count = content.count("in\n") + content.count("in\r\n") + content.count(" in ") + (1 if content.strip().endswith("in") else 0)
            self.assertGreaterEqual(let_count, 1, f"{pq_file.name} missing 'let'")
            self.assertGreaterEqual(in_count, 1, f"{pq_file.name} missing 'in'")

    def test_abn_validator_m_logic(self) -> None:
        """Verify Fx_ValidateABN.pq references the statutory ATO weights and Modulus 89."""
        abn_pq = PQ_DIR / "Fx_ValidateABN.pq"
        self.assertTrue(abn_pq.is_file(), "Fx_ValidateABN.pq must exist")
        content = abn_pq.read_text(encoding="utf-8")
        self.assertIn("10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19", content)
        self.assertIn("Number.Mod", content)
        self.assertIn("89", content)

    def test_csv_source_column_counts_match_fixture_rows(self) -> None:
        cases = {
            "Dim_Account.pq": "sample-chart-of-accounts.csv",
            "Dim_Entity.pq": "sample-entities.csv",
            "Fact_PayrollSuper.pq": "sample-payroll-super.csv",
        }

        for query_name, sample_name in cases.items():
            with self.subTest(query=query_name):
                content = (PQ_DIR / query_name).read_text(encoding="utf-8")
                match = re.search(r"\bColumns=(\d+)\b", content)
                self.assertIsNotNone(match, f"{query_name} must declare its CSV width")
                declared_columns = int(match.group(1))  # type: ignore[union-attr]

                with (SAMPLES_DIR / sample_name).open(
                    newline="", encoding="utf-8"
                ) as handle:
                    fixture_widths = {len(row) for row in csv.reader(handle)}

                self.assertEqual(
                    fixture_widths,
                    {declared_columns},
                    f"{query_name} declares {declared_columns} columns but "
                    f"{sample_name} has row widths {sorted(fixture_widths)}",
                )

    def test_dim_account_preserves_quoted_account_name(self) -> None:
        content = (PQ_DIR / "Dim_Account.pq").read_text(encoding="utf-8")
        self.assertIn("QuoteStyle=QuoteStyle.Csv", content)

        with (SAMPLES_DIR / "sample-chart-of-accounts.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            account = next(row for row in csv.reader(handle) if row[0] == "200")

        self.assertEqual(len(account), 9)
        self.assertEqual(account[1], "Property, Plant & Equipment")


if __name__ == "__main__":
    unittest.main()
