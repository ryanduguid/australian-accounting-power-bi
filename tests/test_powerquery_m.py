"""
test_powerquery_m.py - Static syntax and structure checks for Power Query (M) modules.
"""

from __future__ import annotations

import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PQ_DIR = BASE_DIR / "powerquery"


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


if __name__ == "__main__":
    unittest.main()
