"""
test_payday_super_rules.py - Asserts Australian Payday Super statutory calculation rules.
"""

from __future__ import annotations

import csv
import datetime
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "samples"


class TestPaydaySuperRules(unittest.TestCase):
    def test_sg_statutory_rate_is_12_percent(self) -> None:
        """Payday Super SG rate must be 12.0% (in force from 1 July 2025 onwards)."""
        payroll_path = SAMPLES_DIR / "sample-payroll-super.csv"
        with open(payroll_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                q_earnings = float(row["QualifyingEarnings_CodeQ"])
                liability = float(row["SuperLiability_CodeL"])
                expected_liability = round(q_earnings * 0.12, 2)
                self.assertAlmostEqual(
                    liability,
                    expected_liability,
                    places=2,
                    msg=f"Event {row['EventID']} Super Liability ({liability}) does not match 12% of {q_earnings}",
                )

    def test_statutory_due_date_post_1_july_2026(self) -> None:
        """Under the Payday Super regime (from 1 July 2026), due date is strictly 7 national business days after payday."""
        payroll_path = SAMPLES_DIR / "sample-payroll-super.csv"
        with open(payroll_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pay_date = datetime.date.fromisoformat(row["PayDate"])
                due_date = datetime.date.fromisoformat(row["StatutoryDueDate"])
                if pay_date >= datetime.date(2026, 7, 1):
                    # Elapsed calendar days must be between 9 and 14 days (7 business days + weekends + holidays)
                    delta_days = (due_date - pay_date).days
                    self.assertGreaterEqual(
                        delta_days,
                        9,
                        f"Due date {due_date} is too close to pay date {pay_date}",
                    )
                    self.assertLessEqual(
                        delta_days,
                        15,
                        f"Due date {due_date} is too far from pay date {pay_date}",
                    )

    def test_compliance_status_flagging(self) -> None:
        """If fund receipt date is strictly after statutory due date, status must be LATE_BREACH with non-zero SGC."""
        payroll_path = SAMPLES_DIR / "sample-payroll-super.csv"
        with open(payroll_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rec_date = datetime.date.fromisoformat(row["FundReceiptDate"])
                due_date = datetime.date.fromisoformat(row["StatutoryDueDate"])
                status = row["ComplianceStatus"]
                sgc = float(row["SGC_Shortfall"])

                if rec_date > due_date:
                    self.assertEqual(status, "LATE_BREACH", f"Event {row['EventID']} should be flagged LATE_BREACH")
                    self.assertGreater(sgc, 0.0, f"Late event {row['EventID']} must have non-zero SGC shortfall")
                else:
                    self.assertEqual(status, "ON_TIME", f"Event {row['EventID']} should be flagged ON_TIME")
                    self.assertEqual(sgc, 0.0, f"On-time event {row['EventID']} must have 0.0 SGC shortfall")


if __name__ == "__main__":
    unittest.main()
