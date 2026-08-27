# Australian Accounting Power BI

[![Verify](https://github.com/ryanduguid/australian-accounting-power-bi/actions/workflows/verify.yml/badge.svg)](https://github.com/ryanduguid/australian-accounting-power-bi/actions/workflows/verify.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Status: incubating.** This source-controlled Power BI Project (`.pbip`) is an evolving reference implementation, not a production-ready Power BI solution. It demonstrates Australian accounting domain modelling, dimensional star schema design, Tabular Model Definition Language (TMDL), calculation groups, and automated GitHub Actions CI verification.

---

## What This Project Solves

Most Power BI repositories on GitHub commit monolithic binary `.pbix` blobs with zero diffability, no automated test suites, and generic mock sales data.

This project treats Power BI as source-controlled software engineering:
1. **Plain-Text Version Control**: Built entirely on the Power BI Project format (`.pbip`), using Tabular Model Definition Language (`.tmdl`) and Enhanced Report Format (`.pbir`). Every measure, visual, relationship, and M partition produces clean, reviewable git diffs.
2. **3-Way Financial Statements & Multi-Entity Consolidation**: P&L, Balance Sheet, and Cash Flow matrix reporting across a multi-entity corporate group (operating company, trading subsidiary, logistics entity, property trust) with automated intercompany transaction eliminations.
3. **ATO Small Business Benchmarks Diagnostic**: Ingests ANZSIC industry classifications and scores business cost structures against official Australian Taxation Office benchmark bands and PCG 2026/1 compliance risk zones.
4. **Live Payday Super Compliance Monitoring**: Tracks Single Touch Payroll Phase 2 events (Code Q - Qualifying Earnings, Code L - Super Liability at 12.0%) against the statutory 7-business-day fund receipt rule commencing 1 July 2026, including automated SGC shortfall and GIC nominal interest exposure calculators.

---

## Data Model Architecture (Star Schema)

```mermaid
erDiagram
    Dim_Entity ||--o{ Fact_GeneralLedger : "EntityID"
    Dim_Entity ||--o{ Fact_Budget : "EntityID"
    Dim_Entity ||--o{ Fact_PayrollSuper : "EntityID"
    Dim_Entity ||--o{ Dim_ANZSIC : "ANZSIC_Code"
    
    Dim_Account ||--o{ Fact_GeneralLedger : "AccountCode"
    Dim_Account ||--o{ Fact_Budget : "AccountCode"
    
    Dim_Date ||--o{ Fact_GeneralLedger : "PostingDate"
    Dim_Date ||--o{ Fact_Budget : "PeriodDate"
    Dim_Date ||--o{ Fact_PayrollSuper : "PayDate"
    
    Dim_Employee ||--o{ Fact_PayrollSuper : "EmployeeID"
    
    Dim_ANZSIC ||--o{ Fact_ATOBenchmark : "ANZSIC_Code"
```

See [docs/data-model.md](docs/data-model.md) for table grain, schema descriptions, and dimension attributes.

---

## Report Structure (4 Pages)

1. **Executive 3-Way Financial Performance**: Consolidated P&L, Balance Sheet, and Direct/Indirect Cash Flow bridge with interactive entity and period slicing.
2. **Multi-Entity Consolidation & Eliminations**: Entity-level matrix views with automated intra-group elimination columns and intercompany loan audit trails.
3. **ATO Benchmark & Practice Diagnostic**: ANZSIC industry quantile comparisons, gross margin and cost ratio variance analyses, and automated PCG 2026/1 audit risk ratings.
4. **Payday Super & STP Compliance Monitor**: 7-business-day timeline tracker, clearing-house transit risk analyser, and estimated Super Guarantee Charge (SGC) exposure calculators.

---

## Calculation Groups & Advanced DAX

The semantic model uses calculation groups to dynamically apply time intelligence and consolidation filters across any base measure without measure proliferation:

- **`CalcGroup_TimeIntelligence`**: Supports Base Period, MTD, QTD, FYTD (1 July to 30 June Australian financial year), Prior Year (PY), YoY Variance (\$), and YoY Variance (%).
- **`CalcGroup_Consolidation`**: Supports Gross Group Total, Intercompany Eliminations, and Consolidated Group Net.

See [docs/dax-patterns.md](docs/dax-patterns.md) for full DAX formulas and precedence rules.

---

## Repository Layout

```text
australian-accounting-power-bi/
├── .github/
│   └── workflows/
│       └── verify.yml                   # CI: TMDL schema validation & fixture balance check
├── docs/
│   ├── data-model.md                    # Star schema diagram & dimension specifications
│   ├── dax-patterns.md                  # Calculation groups & financial statement DAX
│   └── compliance-methodology.md        # Australian tax & Payday Super calculation rules
├── australian-accounting-power-bi.pbip  # Power BI Project root descriptor
├── australian-accounting-power-bi.Report/ # Enhanced Report Format (PBIR)
│   ├── definition.pbir
│   └── definition/
│       └── report.json                  # Canvas themes, page layouts, visual configs
├── australian-accounting-power-bi.SemanticModel/ # Tabular Model Definition Language (TMDL)
│   ├── definition.tmdl
│   ├── model.tmdl
│   ├── relationships.tmdl               # Unidirectional star schema relationships
│   └── tables/                          # One TMDL file per dimension, fact, and calculation group
├── powerquery/                          # Standalone Power Query (M) transformations
│   ├── Dim_Date_AU.pq                   # Australian Financial Year generator (1 Jul - 30 Jun)
│   ├── Fx_ValidateABN.pq                # Statutory ATO ABN Modulus-89 checksum validator
│   ├── Fact_GeneralLedger.pq            # GL ingestion and staging query
│   └── Fact_PayrollSuper.pq             # STP & Payday Super staging query
├── samples/                             # Deterministic fabricated CSV fixtures
│   ├── sample-entities.csv              # Varrock Ventures, Draynor Produce, Falador Freight
│   ├── sample-chart-of-accounts.csv     # Standard Australian Chart of Accounts
│   ├── sample-general-ledger.csv        # Balanced double-entry GL journals (FY25-FY27)
│   ├── sample-budgets.csv               # Monthly departmental budgets
│   ├── sample-payroll-super.csv         # Payday Super events with on-time & late receipts
│   └── sample-ato-benchmarks.csv        # Real ATO benchmark percentiles by ANZSIC category
├── tests/
│   ├── test_fixtures_balance.py         # Asserts debits == credits per journal and period
│   ├── test_tmdl_integrity.py           # Asserts TMDL syntax, explicit measure formats, descriptions
│   ├── test_powerquery_m.py             # Validates Power Query M syntax and structure
│   ├── test_payday_super_rules.py       # Verifies Payday Super 7-business-day statutory rules
│   └── model_bpa_rules.json             # Tabular Model Best Practice Analyzer ruleset
├── tools/
│   └── generate_fixtures.py             # Script to deterministically generate all synthetic test data
├── LICENSE                              # MIT License
├── DISCLAIMER.md                        # Professional disclaimer
├── CONTRIBUTING.md                      # Contribution guidelines
└── SECURITY.md                          # Security policy
```

---

## Verification & Automated Testing

Run the test suite locally:

```bash
python -B -m unittest discover -s tests -v
```

The test suite verifies:
- Every journal in `sample-general-ledger.csv` balances to zero (debits equal credits).
- Intercompany entries balance to zero across the group.
- Every DAX measure in TMDL contains explicit `formatString` and `description` metadata.
- All relationships enforce strict single-direction star schema filtering.
- Power Query M scripts contain valid balanced `let ... in` expressions and valid ABN algorithm weights.
- Payday Super tests assert 12.0% SG rate, 7-business-day national calendar calculation, and leap year GIC divisors (366 days in leap years per s 8AAD TAA).

---

## Opening the Project

1. Open `australian-accounting-power-bi.pbip` in **Power BI Desktop** (Developer Mode enabled).
2. Or inspect and edit the semantic model directly in **Tabular Editor 3 / 2** by opening the `australian-accounting-power-bi.SemanticModel` directory.
3. Or view and edit TMDL files in **Visual Studio Code** using the Microsoft TMDL extension.

---

## Disclaimer

Utility code, MIT-licensed, no warranty. Nothing here constitutes tax, financial, or legal advice. Outputs and calculations require independent professional review. All sample data is fabricated using synthetic entities.

---

## Author

Ryan Duguid, accountant in Newcastle NSW, provisional member of Chartered Accountants ANZ.
