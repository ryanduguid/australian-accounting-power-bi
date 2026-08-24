# Statutory & Compliance Methodology

This document details the Australian statutory frameworks, tax laws, and accounting standards modelled in `au-financial-analytics-pbip`.

---

## 1. Payday Superannuation Regime (In Force 1 July 2026)

### Enabling Legislation
- *Superannuation Guarantee (Administration) Amendment Act No. 57 of 2025* (Royal Assent 6 November 2025).
- Live commencement: **1 July 2026**.

### Statutory 7-Business-Day Rule
1. **Due Date Test**: Contributions must be **received by the employee's superannuation fund** within **7 business days** after payday (20 business days for new employees or newly nominated funds).
2. **Transit Risk**: Remittance to a commercial clearing house on day 6 is non-compliant if the fund receives the money on day 8. Transit time is the employer's risk.
3. **National Business Day Calendar**: A business day excludes Saturdays, Sundays, and any public holiday gazetted for the **whole of any State or Territory**. Regional holidays (e.g. Brisbane Ekka, Melbourne Cup regional gazettals) do not stop the national clock.

### Base Earnings & Rates
- **Statutory SG Rate**: **12.0%** (effective since 1 July 2025).
- **Qualifying Earnings (Code Q)**: Replaces Ordinary Time Earnings (OTE) as the statutory SG base from 1 July 2026.
- **Single Touch Payroll (STP Phase 2)**:
  - `Code Q`: Qualifying earnings paid in the pay run.
  - `Code L`: Superannuation liability accrued in the pay run.

### Superannuation Guarantee Charge (SGC) & GIC
- If late, the employer incurs an SGC shortfall liability consisting of:
  1. SG shortfall based on total salary and wages (not just qualifying earnings).
  2. Nominal interest compounding daily at the General Interest Charge (GIC) rate from the first day of the relevant quarter.
  3. Administration fee (\$20 per employee per quarter/event).
- **Leap Year Divisor**: Per Section 8AAD of the *Taxation Administration Act 1953*, the daily GIC divisor is the exact number of days in the calendar year (**366 in leap years** such as 2024, 365 in non-leap years).
- **Tax Deductibility**: Under the amended regime, statutory SG charges are tax-deductible.

---

## 2. ATO Small Business Benchmarks (PCG 2026/1 Framework)

### ANZSIC Benchmarking
The ATO publishes financial performance benchmarks across turnover bands for small businesses based on income tax returns and activity statements.

### Key Ratios Monitored
1. **Gross Profit Margin %**: `(Sales - Cost of Goods Sold) / Sales`
2. **Total Expenses Ratio %**: `Operating Expenses / Sales`
3. **Labour Cost Ratio %**: `(Salaries + Superannuation) / Sales`
4. **Rent Ratio %**: `Rent Expense / Sales`
5. **Motor Vehicle Expense Ratio %**: `Motor Vehicle Running Costs / Sales`

### Compliance Risk Profiling
- **Green Zone (Within Benchmark)**: Normal compliance monitoring.
- **Amber Zone (Moderate Variance 4% to 8%)**: Potential record-keeping review.
- **Red Zone (High Variance > 8%)**: Elevated ATO audit and compliance resource allocation risk. Practical Compliance Guideline PCG 2026/1 notes risk zones govern ATO compliance resourcing, not automatic liability.

---

## 3. Multi-Entity Consolidation (AASB 10)

### Intercompany Elimination Principle
Where entities within a corporate group trade with each other (e.g. parent company charging subsidiary management fees, or logistics entity hauling goods for retail entity), intra-group transactions must be eliminated to present the true third-party consolidated group financial position.

- **P&L Eliminations**: Intra-group revenue (Account 650) debited against intra-group expense (Account 880 / 750).
- **Balance Sheet Eliminations**: Intercompany loan assets (Account 180) credited against intercompany loan liabilities (Account 380).
- The net effect of all elimination journals across a balanced group is exactly **$0.00**.
