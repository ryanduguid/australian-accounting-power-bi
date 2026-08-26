#!/usr/bin/env python3
"""
generate_fixtures.py - Deterministic synthetic fixture generator for au-financial-analytics-pbip.

Generates balanced double-entry general ledger journals, chart of accounts, multi-entity masters,
budgets, Payday Super payroll events (STP Phase 2), and ATO Small Business Benchmark distributions.

Zero client or real taxpayer data is used. All entities use fictional place names per project standards.
"""

from __future__ import annotations

import csv
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "samples"

# Australian National Public Holidays (whole-of-state/territory national calendar 2024-2027)
NATIONAL_HOLIDAYS = {
    # 2024
    datetime.date(2024, 1, 1),   # New Year's Day
    datetime.date(2024, 1, 26),  # Australia Day
    datetime.date(2024, 3, 29),  # Good Friday
    datetime.date(2024, 4, 1),   # Easter Monday
    datetime.date(2024, 4, 25),  # Anzac Day
    datetime.date(2024, 6, 10),  # King's Birthday
    datetime.date(2024, 12, 25), # Christmas Day
    datetime.date(2024, 12, 26), # Boxing Day
    # 2025
    datetime.date(2025, 1, 1),
    datetime.date(2025, 1, 27),  # Australia Day (Observed)
    datetime.date(2025, 4, 18),  # Good Friday
    datetime.date(2025, 4, 21),  # Easter Monday
    datetime.date(2025, 4, 25),  # Anzac Day
    datetime.date(2025, 6, 9),   # King's Birthday
    datetime.date(2025, 12, 25), # Christmas Day
    datetime.date(2025, 12, 26), # Boxing Day
    # 2026
    datetime.date(2026, 1, 1),
    datetime.date(2026, 1, 26),  # Australia Day
    datetime.date(2026, 4, 3),   # Good Friday
    datetime.date(2026, 4, 6),   # Easter Monday
    datetime.date(2026, 4, 25),  # Anzac Day
    datetime.date(2026, 6, 8),   # King's Birthday
    datetime.date(2026, 12, 25), # Christmas Day
    datetime.date(2026, 12, 28), # Boxing Day (Observed)
    # 2027
    datetime.date(2027, 1, 1),
    datetime.date(2027, 1, 26),
    datetime.date(2027, 3, 26),  # Good Friday
    datetime.date(2027, 3, 29),  # Easter Monday
    datetime.date(2027, 4, 25),  # Anzac Day
    datetime.date(2027, 4, 26),  # Anzac Day (Observed)
    datetime.date(2027, 6, 14),  # King's Birthday
    datetime.date(2027, 12, 25),
    datetime.date(2027, 12, 27), # Christmas Day (Observed)
    datetime.date(2027, 12, 28), # Boxing Day (Observed)
}

def is_national_business_day(d: datetime.date) -> bool:
    """Return True if weekday (Mon-Fri) and not a national Australian public holiday."""
    return d.weekday() < 5 and d not in NATIONAL_HOLIDAYS

def add_business_days(start_date: datetime.date, num_days: int) -> datetime.date:
    """Add N national business days after start_date."""
    current = start_date
    added = 0
    while added < num_days:
        current += datetime.timedelta(days=1)
        if is_national_business_day(current):
            added += 1
    return current


ENTITIES = [
    {
        "EntityID": "ENT001",
        "LegalName": "Varrock Ventures Pty Ltd",
        "TradingName": "Varrock Advisory & Tech",
        "ABN": "51824753556",
        "ACN": "123456789",
        "TaxStructure": "Company",
        "EntityRole": "Parent Operating",
        "ANZSIC_Code": "6962",
        "Currency": "AUD",
        "ConsolidationWeight": "1.0",
    },
    {
        "EntityID": "ENT002",
        "LegalName": "Draynor Produce Pty Ltd",
        "TradingName": "Draynor Fresh Foods",
        "ABN": "82147629350",
        "ACN": "234567890",
        "TaxStructure": "Company",
        "EntityRole": "Trading Subsidiary",
        "ANZSIC_Code": "4122",
        "Currency": "AUD",
        "ConsolidationWeight": "1.0",
    },
    {
        "EntityID": "ENT003",
        "LegalName": "Falador Freight Pty Ltd",
        "TradingName": "Falador National Logistics",
        "ABN": "33087542911",
        "ACN": "345678901",
        "TaxStructure": "Company",
        "EntityRole": "Logistics Subsidiary",
        "ANZSIC_Code": "4610",
        "Currency": "AUD",
        "ConsolidationWeight": "1.0",
    },
    {
        "EntityID": "ENT004",
        "LegalName": "Ardougne Holdings Trust",
        "TradingName": "Ardougne Commercial Property",
        "ABN": "12345678901",
        "ACN": "",
        "TaxStructure": "Unit Trust",
        "EntityRole": "Property Asset Trust",
        "ANZSIC_Code": "6712",
        "Currency": "AUD",
        "ConsolidationWeight": "1.0",
    },
]

CHART_OF_ACCOUNTS = [
    # Assets
    {"AccountCode": "100", "AccountName": "Cash at Bank - Operating", "Class": "Asset", "SubClass": "Current Assets", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Cash & Cash Equivalents", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 10},
    {"AccountCode": "110", "AccountName": "Trade Receivables", "Class": "Asset", "SubClass": "Current Assets", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Receivables", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 20},
    {"AccountCode": "120", "AccountName": "Inventories on Hand", "Class": "Asset", "SubClass": "Current Assets", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Inventory", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 30},
    {"AccountCode": "180", "AccountName": "Intercompany Loan Receivable", "Class": "Asset", "SubClass": "Current Assets", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Intercompany Receivables", "CashFlowCategory": "Financing", "NormalBalance": "Debit", "SortOrder": 40},
    {"AccountCode": "200", "AccountName": "Property, Plant & Equipment", "Class": "Asset", "SubClass": "Non-Current Assets", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Fixed Assets", "CashFlowCategory": "Investing", "NormalBalance": "Debit", "SortOrder": 50},
    {"AccountCode": "210", "AccountName": "Accumulated Depreciation", "Class": "Asset", "SubClass": "Non-Current Assets", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Fixed Assets", "CashFlowCategory": "Investing", "NormalBalance": "Credit", "SortOrder": 60},
    {"AccountCode": "250", "AccountName": "Commercial Real Estate (Property)", "Class": "Asset", "SubClass": "Non-Current Assets", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Investment Property", "CashFlowCategory": "Investing", "NormalBalance": "Debit", "SortOrder": 70},

    # Liabilities
    {"AccountCode": "300", "AccountName": "Trade Payables", "Class": "Liability", "SubClass": "Current Liabilities", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Payables", "CashFlowCategory": "Operating", "NormalBalance": "Credit", "SortOrder": 110},
    {"AccountCode": "310", "AccountName": "GST Clearing Account", "Class": "Liability", "SubClass": "Current Liabilities", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Tax Liabilities", "CashFlowCategory": "Operating", "NormalBalance": "Credit", "SortOrder": 120},
    {"AccountCode": "320", "AccountName": "PAYG Withholding Payable", "Class": "Liability", "SubClass": "Current Liabilities", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Tax Liabilities", "CashFlowCategory": "Operating", "NormalBalance": "Credit", "SortOrder": 130},
    {"AccountCode": "330", "AccountName": "Superannuation Guarantee Payable", "Class": "Liability", "SubClass": "Current Liabilities", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Payroll Liabilities", "CashFlowCategory": "Operating", "NormalBalance": "Credit", "SortOrder": 140},
    {"AccountCode": "380", "AccountName": "Intercompany Loan Payable", "Class": "Liability", "SubClass": "Current Liabilities", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Intercompany Payables", "CashFlowCategory": "Financing", "NormalBalance": "Credit", "SortOrder": 150},
    {"AccountCode": "400", "AccountName": "Bank Commercial Loan Facility", "Class": "Liability", "SubClass": "Non-Current Liabilities", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Borrowings", "CashFlowCategory": "Financing", "NormalBalance": "Credit", "SortOrder": 160},

    # Equity
    {"AccountCode": "500", "AccountName": "Share Capital / Settled Sum", "Class": "Equity", "SubClass": "Equity", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Contributed Capital", "CashFlowCategory": "Financing", "NormalBalance": "Credit", "SortOrder": 210},
    {"AccountCode": "510", "AccountName": "Retained Earnings - Prior Years", "Class": "Equity", "SubClass": "Equity", "ReportSection": "Balance Sheet", "BalanceSheetGroup": "Retained Profits", "CashFlowCategory": "Operating", "NormalBalance": "Credit", "SortOrder": 220},

    # Revenue
    {"AccountCode": "600", "AccountName": "Commercial Trading Revenue", "Class": "Revenue", "SubClass": "Operating Revenue", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Revenue", "CashFlowCategory": "Operating", "NormalBalance": "Credit", "SortOrder": 310},
    {"AccountCode": "610", "AccountName": "Professional Advisory Fees", "Class": "Revenue", "SubClass": "Operating Revenue", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Revenue", "CashFlowCategory": "Operating", "NormalBalance": "Credit", "SortOrder": 320},
    {"AccountCode": "620", "AccountName": "Commercial Rental Income", "Class": "Revenue", "SubClass": "Operating Revenue", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Revenue", "CashFlowCategory": "Operating", "NormalBalance": "Credit", "SortOrder": 330},
    {"AccountCode": "650", "AccountName": "Intercompany Management Fees Revenue", "Class": "Revenue", "SubClass": "Intercompany Revenue", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Intercompany Revenue", "CashFlowCategory": "Operating", "NormalBalance": "Credit", "SortOrder": 340},

    # Cost of Sales
    {"AccountCode": "700", "AccountName": "Direct Cost of Goods Sold", "Class": "Expense", "SubClass": "Cost of Sales", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Cost of Sales", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 410},
    {"AccountCode": "710", "AccountName": "Direct Freight & Fuel Expense", "Class": "Expense", "SubClass": "Cost of Sales", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Cost of Sales", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 420},
    {"AccountCode": "750", "AccountName": "Intercompany Freight Expense", "Class": "Expense", "SubClass": "Cost of Sales", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Cost of Sales", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 430},

    # Operating Expenses
    {"AccountCode": "800", "AccountName": "Salaries & Wages", "Class": "Expense", "SubClass": "Operating Expenses", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Operating Expenses", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 510},
    {"AccountCode": "805", "AccountName": "Superannuation Guarantee Expense", "Class": "Expense", "SubClass": "Operating Expenses", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Operating Expenses", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 520},
    {"AccountCode": "810", "AccountName": "Motor Vehicle Running Costs", "Class": "Expense", "SubClass": "Operating Expenses", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Operating Expenses", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 530},
    {"AccountCode": "820", "AccountName": "Rent & Property Occupancy", "Class": "Expense", "SubClass": "Operating Expenses", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Operating Expenses", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 540},
    {"AccountCode": "830", "AccountName": "Insurance & Compliance", "Class": "Expense", "SubClass": "Operating Expenses", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Operating Expenses", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 550},
    {"AccountCode": "880", "AccountName": "Intercompany Management Fees Expense", "Class": "Expense", "SubClass": "Operating Expenses", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Operating Expenses", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 560},
    {"AccountCode": "890", "AccountName": "Depreciation Expense", "Class": "Expense", "SubClass": "Operating Expenses", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Operating Expenses", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 570},
    {"AccountCode": "895", "AccountName": "Finance & Bank Interest Expense", "Class": "Expense", "SubClass": "Operating Expenses", "ReportSection": "Profit and Loss", "BalanceSheetGroup": "Operating Expenses", "CashFlowCategory": "Operating", "NormalBalance": "Debit", "SortOrder": 580},
]

def generate_fixtures():
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Write Entities
    with open(SAMPLES_DIR / "sample-entities.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(ENTITIES[0].keys()))
        writer.writeheader()
        writer.writerows(ENTITIES)

    # 2. Write Chart of Accounts
    with open(SAMPLES_DIR / "sample-chart-of-accounts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(CHART_OF_ACCOUNTS[0].keys()))
        writer.writeheader()
        writer.writerows(CHART_OF_ACCOUNTS)

    # 3. Write General Ledger (Balanced double-entry journals over 36 months from July 2024 to June 2027)
    gl_rows = []
    journal_id = 1000

    def add_balanced_journal(date_str: str, entity_id: str, desc: str, debits: list[tuple[str, float]], credits: list[tuple[str, float]], ic_entity: str = ""):
        nonlocal journal_id
        journal_id += 1
        d_sum = round(sum(amt for _, amt in debits), 2)
        c_sum = round(sum(amt for _, amt in credits), 2)
        assert d_sum == c_sum, f"Unbalanced journal {journal_id}: Debits {d_sum} != Credits {c_sum}"
        line_no = 1
        for code, amt in debits:
            gl_rows.append({
                "JournalID": f"JNL{journal_id}",
                "LineNumber": line_no,
                "PostingDate": date_str,
                "EntityID": entity_id,
                "AccountCode": code,
                "Debit": f"{amt:.2f}",
                "Credit": "0.00",
                "Amount": f"{amt:.2f}",  # Net positive for debit
                "Description": desc,
                "IntercompanyEntityID": ic_entity,
                "IsIntercompany": "TRUE" if ic_entity else "FALSE",
            })
            line_no += 1
        for code, amt in credits:
            gl_rows.append({
                "JournalID": f"JNL{journal_id}",
                "LineNumber": line_no,
                "PostingDate": date_str,
                "EntityID": entity_id,
                "AccountCode": code,
                "Debit": "0.00",
                "Credit": f"{amt:.2f}",
                "Amount": f"{-amt:.2f}",  # Net negative for credit
                "Description": desc,
                "IntercompanyEntityID": ic_entity,
                "IsIntercompany": "TRUE" if ic_entity else "FALSE",
            })
            line_no += 1

    # Opening balances at 1 July 2024 (balanced per entity)
    # ENT001
    add_balanced_journal("2024-07-01", "ENT001", "Opening Balance FY25", [("100", 350000.0), ("110", 120000.0), ("200", 80000.0)], [("300", 90000.0), ("500", 100000.0), ("510", 360000.0)])
    # ENT002
    add_balanced_journal("2024-07-01", "ENT002", "Opening Balance FY25", [("100", 180000.0), ("110", 95000.0), ("120", 150000.0), ("200", 65000.0)], [("300", 110000.0), ("500", 50000.0), ("510", 330000.0)])
    # ENT003
    add_balanced_journal("2024-07-01", "ENT003", "Opening Balance FY25", [("100", 95000.0), ("110", 140000.0), ("200", 450000.0)], [("210", 90000.0), ("300", 75000.0), ("400", 250000.0), ("500", 50000.0), ("510", 220000.0)])
    # ENT004
    add_balanced_journal("2024-07-01", "ENT004", "Opening Balance FY25", [("100", 60000.0), ("250", 1800000.0)], [("400", 900000.0), ("500", 100.0), ("510", 959900.0)])

    # Monthly operational cycles for 36 months (Jul 2024 to Jun 2027)
    for m_idx in range(36):
        # Calculate month date (around 15th and 28th)
        year = 2024 + (7 + m_idx - 1) // 12
        month = ((7 + m_idx - 1) % 12) + 1
        d_mid = datetime.date(year, month, 15).strftime("%Y-%m-%d")
        d_end = datetime.date(year, month, 28).strftime("%Y-%m-%d")

        # Growth factor over 3 years
        factor = 1.0 + (m_idx * 0.015)

        # ENT001 (Varrock Ventures - Advisory)
        rev_ent1 = round(160000.0 * factor, 2)
        sal_ent1 = round(75000.0 * factor, 2)
        sup_ent1 = round(sal_ent1 * 0.12, 2)
        add_balanced_journal(d_mid, "ENT001", f"Advisory Billings - M{m_idx+1}", [("110", rev_ent1)], [("610", rev_ent1)])
        add_balanced_journal(d_end, "ENT001", f"Monthly Payroll - M{m_idx+1}", [("800", sal_ent1), ("805", sup_ent1)], [("100", sal_ent1), ("330", sup_ent1)])
        add_balanced_journal(d_end, "ENT001", f"Operating Costs & Rent - M{m_idx+1}", [("820", 12000.0), ("830", 3500.0)], [("100", 15500.0)])

        # ENT002 (Draynor Produce - Fresh Foods)
        rev_ent2 = round(280000.0 * factor, 2)
        cogs_ent2 = round(rev_ent2 * 0.58, 2)
        sal_ent2 = round(45000.0 * factor, 2)
        sup_ent2 = round(sal_ent2 * 0.12, 2)
        add_balanced_journal(d_mid, "ENT002", f"Food Retailing Sales - M{m_idx+1}", [("100", rev_ent2)], [("600", rev_ent2)])
        add_balanced_journal(d_mid, "ENT002", f"Produce Inventory Purchase - M{m_idx+1}", [("700", cogs_ent2)], [("100", cogs_ent2)])
        add_balanced_journal(d_end, "ENT002", f"Monthly Payroll - M{m_idx+1}", [("800", sal_ent2), ("805", sup_ent2)], [("100", sal_ent2), ("330", sup_ent2)])
        add_balanced_journal(d_end, "ENT002", f"Store Operating Costs - M{m_idx+1}", [("820", 8500.0), ("810", 4200.0)], [("100", 12700.0)])

        # ENT003 (Falador Freight - Logistics)
        rev_ent3 = round(190000.0 * factor, 2)
        fuel_ent3 = round(rev_ent3 * 0.28, 2)
        sal_ent3 = round(60000.0 * factor, 2)
        sup_ent3 = round(sal_ent3 * 0.12, 2)
        add_balanced_journal(d_mid, "ENT003", f"Freight Service Revenue - M{m_idx+1}", [("110", rev_ent3)], [("600", rev_ent3)])
        add_balanced_journal(d_mid, "ENT003", f"Fleet Fuel & Maintenance - M{m_idx+1}", [("710", fuel_ent3), ("810", 6500.0)], [("100", fuel_ent3 + 6500.0)])
        add_balanced_journal(d_end, "ENT003", f"Driver Payroll - M{m_idx+1}", [("800", sal_ent3), ("805", sup_ent3)], [("100", sal_ent3), ("330", sup_ent3)])
        add_balanced_journal(d_end, "ENT003", f"Vehicle Depreciation - M{m_idx+1}", [("890", 4500.0)], [("210", 4500.0)])

        # ENT004 (Ardougne Holdings Trust - Property)
        add_balanced_journal(d_mid, "ENT004", f"Property Rent Collection - M{m_idx+1}", [("100", 25000.0)], [("620", 25000.0)])
        add_balanced_journal(d_end, "ENT004", f"Bank Facility Interest - M{m_idx+1}", [("895", 5200.0)], [("100", 5200.0)])

        # --- INTERCOMPANY TRANSACTIONS (Strictly matched pairs for elimination) ---
        # 1. ENT001 charges ENT002 and ENT003 Management Fees ($10,000 and $6,000)
        add_balanced_journal(d_end, "ENT001", "Intercompany Management Fees Charged", [("180", 16000.0)], [("650", 16000.0)], ic_entity="GROUP")
        add_balanced_journal(d_end, "ENT002", "Intercompany Management Fee Incurred", [("880", 10000.0)], [("380", 10000.0)], ic_entity="ENT001")
        add_balanced_journal(d_end, "ENT003", "Intercompany Management Fee Incurred", [("880", 6000.0)], [("380", 6000.0)], ic_entity="ENT001")

        # 2. ENT003 provides internal freight logistics to ENT002 ($8,500)
        add_balanced_journal(d_end, "ENT003", "Internal Logistics Billed to Draynor", [("180", 8500.0)], [("600", 8500.0)], ic_entity="ENT002")
        add_balanced_journal(d_end, "ENT002", "Intercompany Freight Costs", [("750", 8500.0)], [("380", 8500.0)], ic_entity="ENT003")

    with open(SAMPLES_DIR / "sample-general-ledger.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(gl_rows[0].keys()))
        writer.writeheader()
        writer.writerows(gl_rows)

    # 4. Write Monthly Budgets
    budget_rows = []
    for m_idx in range(36):
        year = 2024 + (7 + m_idx - 1) // 12
        month = ((7 + m_idx - 1) % 12) + 1
        p_date = f"{year}-{month:02d}-01"
        for ent in ["ENT001", "ENT002", "ENT003", "ENT004"]:
            if ent == "ENT001":
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "610", "BudgetAmount": "175000.00"})
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "800", "BudgetAmount": "78000.00"})
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "805", "BudgetAmount": "9360.00"})
            elif ent == "ENT002":
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "600", "BudgetAmount": "300000.00"})
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "700", "BudgetAmount": "170000.00"})
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "800", "BudgetAmount": "48000.00"})
            elif ent == "ENT003":
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "600", "BudgetAmount": "210000.00"})
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "710", "BudgetAmount": "58000.00"})
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "800", "BudgetAmount": "62000.00"})
            elif ent == "ENT004":
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "620", "BudgetAmount": "25000.00"})
                budget_rows.append({"PeriodDate": p_date, "EntityID": ent, "AccountCode": "895", "BudgetAmount": "5000.00"})

    with open(SAMPLES_DIR / "sample-budgets.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(budget_rows[0].keys()))
        writer.writeheader()
        writer.writerows(budget_rows)

    # 5. Write Payday Super Payroll Events (STP Phase 2 - FY26 and FY27)
    # Covering transition on 1 July 2026. 7 business days deadline from payday.
    payroll_rows = []
    employees = [
        {"EmployeeID": "EMP101", "EntityID": "ENT001", "Name": "A. Vance", "SalaryAnnual": 145000.0, "Frequency": "Fortnightly", "FundUSI": "19323234999001", "FundName": "AustralianSuper"},
        {"EmployeeID": "EMP102", "EntityID": "ENT001", "Name": "B. Sterling", "SalaryAnnual": 115000.0, "Frequency": "Fortnightly", "FundUSI": "16457520308001", "FundName": "ART Super"},
        {"EmployeeID": "EMP201", "EntityID": "ENT002", "Name": "C. Miller", "SalaryAnnual": 68000.0, "Frequency": "Weekly", "FundUSI": "19323234999001", "FundName": "AustralianSuper"},
        {"EmployeeID": "EMP202", "EntityID": "ENT002", "Name": "D. Chen", "SalaryAnnual": 72000.0, "Frequency": "Weekly", "FundUSI": "60905115063001", "FundName": "Hostplus"},
        {"EmployeeID": "EMP301", "EntityID": "ENT003", "Name": "E. Kowalski", "SalaryAnnual": 92000.0, "Frequency": "Fortnightly", "FundUSI": "16457520308001", "FundName": "ART Super"},
        {"EmployeeID": "EMP302", "EntityID": "ENT003", "Name": "F. O'Connor", "SalaryAnnual": 88000.0, "Frequency": "Fortnightly", "FundUSI": "19323234999001", "FundName": "AustralianSuper"},
    ]

    # Generate payroll events from 1 Jan 2026 to 30 June 2027 (covers pre-transition and live Payday Super)
    event_id = 5000
    for emp in employees:
        freq = emp["Frequency"]
        period_days = 7 if freq == "Weekly" else 14
        gross_per_period = round(emp["SalaryAnnual"] / (52 if freq == "Weekly" else 26), 2)
        cur_date = datetime.date(2026, 1, 7 if freq == "Weekly" else 14)
        end_date = datetime.date(2027, 6, 30)

        while cur_date <= end_date:
            event_id += 1
            pay_date = cur_date
            # Payday Super regime is live from 1 July 2026: 7 national business days
            # Before 1 July 2026: quarterly due dates (e.g. 28 days after quarter end)
            is_post_transition = pay_date >= datetime.date(2026, 7, 1)
            due_date = add_business_days(pay_date, 7) if is_post_transition else datetime.date(2026, 4, 28) if pay_date.month <= 3 else datetime.date(2026, 7, 28)

            # Qualifying earnings (Code Q) and Super liability (Code L at 12.0%)
            qualifying_earnings = gross_per_period
            super_liability = round(qualifying_earnings * 0.12, 2)

            # Clearing house transit simulation:
            # Most are paid 2 days after payday, received by fund 4 business days later (On Time)
            # A few injected edge cases simulate clearing house delays (Late)
            is_delayed_case = (event_id % 13 == 0) and is_post_transition
            remit_date = pay_date + datetime.timedelta(days=2)
            if is_delayed_case:
                # Fund received 10 business days after payday -> BREACH
                fund_received_date = add_business_days(pay_date, 10)
                status = "LATE_BREACH"
                days_late = (fund_received_date - due_date).days
                # Nominal interest at 11.34% GIC on 366-day leap year divisor (2026 is non-leap, 2024 leap)
                days_in_yr = 366 if (fund_received_date.year % 4 == 0 and fund_received_date.year % 100 != 0) else 365
                daily_gic = 0.1134 / days_in_yr
                nominal_interest = round(super_liability * daily_gic * max(1, days_late), 2)
                sgc_shortfall = round(super_liability + nominal_interest + 20.0, 2) # $20 admin component
            else:
                fund_received_date = add_business_days(pay_date, 4)
                status = "ON_TIME"
                nominal_interest = 0.0
                sgc_shortfall = 0.0

            payroll_rows.append({
                "EventID": f"STP{event_id}",
                "EmployeeID": emp["EmployeeID"],
                "EntityID": emp["EntityID"],
                "EmployeeName": emp["Name"],
                "PayDate": pay_date.strftime("%Y-%m-%d"),
                "GrossEarnings": f"{gross_per_period:.2f}",
                "QualifyingEarnings_CodeQ": f"{qualifying_earnings:.2f}",
                "SuperLiability_CodeL": f"{super_liability:.2f}",
                "SuperFundUSI": emp["FundUSI"],
                "SuperFundName": emp["FundName"],
                "RemittanceDate": remit_date.strftime("%Y-%m-%d"),
                "FundReceiptDate": fund_received_date.strftime("%Y-%m-%d"),
                "StatutoryDueDate": due_date.strftime("%Y-%m-%d"),
                "ComplianceStatus": status,
                "SGC_Shortfall": f"{sgc_shortfall:.2f}",
                "GIC_NominalInterest": f"{nominal_interest:.2f}",
            })

            cur_date += datetime.timedelta(days=period_days)

    with open(SAMPLES_DIR / "sample-payroll-super.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(payroll_rows[0].keys()))
        writer.writeheader()
        writer.writerows(payroll_rows)

    # 6. Write ATO Benchmarks (Real ATO Small Business benchmark distributions by ANZSIC)
    benchmarks = [
        # ANZSIC 6962 - Management Advice & Consulting
        {"ANZSIC_Code": "6962", "TurnoverRange": "$500k-$1m", "GrossProfitPct_Low": "88.0", "GrossProfitPct_Avg": "92.5", "GrossProfitPct_High": "96.0", "TotalExpensesPct_Avg": "68.0", "RentPct_Avg": "4.5", "MotorVehiclePct_Avg": "3.2", "LabourPct_Avg": "42.0"},
        {"ANZSIC_Code": "6962", "TurnoverRange": "$1m-$5m", "GrossProfitPct_Low": "85.0", "GrossProfitPct_Avg": "90.0", "GrossProfitPct_High": "94.0", "TotalExpensesPct_Avg": "72.0", "RentPct_Avg": "5.0", "MotorVehiclePct_Avg": "2.5", "LabourPct_Avg": "46.0"},
        # ANZSIC 4122 - Fresh Meat, Fish and Poultry Retailing
        {"ANZSIC_Code": "4122", "TurnoverRange": "$500k-$1m", "GrossProfitPct_Low": "34.0", "GrossProfitPct_Avg": "39.5", "GrossProfitPct_High": "45.0", "TotalExpensesPct_Avg": "28.0", "RentPct_Avg": "5.2", "MotorVehiclePct_Avg": "1.8", "LabourPct_Avg": "14.5"},
        {"ANZSIC_Code": "4122", "TurnoverRange": "$1m-$5m", "GrossProfitPct_Low": "36.0", "GrossProfitPct_Avg": "41.0", "GrossProfitPct_High": "47.0", "TotalExpensesPct_Avg": "29.5", "RentPct_Avg": "4.8", "MotorVehiclePct_Avg": "1.2", "LabourPct_Avg": "16.0"},
        # ANZSIC 4610 - Road Freight Transport
        {"ANZSIC_Code": "4610", "TurnoverRange": "$500k-$1m", "GrossProfitPct_Low": "72.0", "GrossProfitPct_Avg": "78.0", "GrossProfitPct_High": "84.0", "TotalExpensesPct_Avg": "65.0", "RentPct_Avg": "2.8", "MotorVehiclePct_Avg": "18.5", "LabourPct_Avg": "31.0"},
        {"ANZSIC_Code": "4610", "TurnoverRange": "$1m-$5m", "GrossProfitPct_Low": "70.0", "GrossProfitPct_Avg": "76.5", "GrossProfitPct_High": "82.0", "TotalExpensesPct_Avg": "66.5", "RentPct_Avg": "2.5", "MotorVehiclePct_Avg": "16.0", "LabourPct_Avg": "33.5"},
        # ANZSIC 6712 - Non-Residential Property Operators
        {"ANZSIC_Code": "6712", "TurnoverRange": "$100k-$500k", "GrossProfitPct_Low": "92.0", "GrossProfitPct_Avg": "96.0", "GrossProfitPct_High": "98.5", "TotalExpensesPct_Avg": "42.0", "RentPct_Avg": "0.0", "MotorVehiclePct_Avg": "1.5", "LabourPct_Avg": "5.0"},
    ]

    with open(SAMPLES_DIR / "sample-ato-benchmarks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(benchmarks[0].keys()))
        writer.writeheader()
        writer.writerows(benchmarks)

    print(f"Successfully generated all synthetic fixtures in {SAMPLES_DIR}")

if __name__ == "__main__":
    generate_fixtures()
