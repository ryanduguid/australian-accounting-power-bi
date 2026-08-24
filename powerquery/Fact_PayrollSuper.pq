// Fact_PayrollSuper.pq
// Ingests Single Touch Payroll (STP Phase 2) events and evaluates Payday Super compliance.

let
    Source = Csv.Document(File.Contents("samples/sample-payroll-super.csv"), [Delimiter=",", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedTable = Table.TransformColumnTypes(PromoteHeaders, {
        {"EventID", type text},
        {"EmployeeID", type text},
        {"EntityID", type text},
        {"EmployeeName", type text},
        {"PayDate", type date},
        {"GrossEarnings", type number},
        {"QualifyingEarnings_CodeQ", type number},
        {"SuperLiability_CodeL", type number},
        {"SuperFundUSI", type text},
        {"SuperFundName", type text},
        {"RemittanceDate", type date},
        {"FundReceiptDate", type date},
        {"StatutoryDueDate", type date},
        {"ComplianceStatus", type text},
        {"SGC_Shortfall", type number},
        {"GIC_NominalInterest", type number}
    })
in
    TypedTable
