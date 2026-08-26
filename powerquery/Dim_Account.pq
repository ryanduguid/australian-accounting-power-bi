// Dim_Account.pq
// Ingests and types the standard Australian Chart of Accounts dimension.

let
    Source = Csv.Document(File.Contents("samples/sample-chart-of-accounts.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedTable = Table.TransformColumnTypes(PromoteHeaders, {
        {"AccountCode", type text},
        {"AccountName", type text},
        {"Class", type text},
        {"SubClass", type text},
        {"ReportSection", type text},
        {"BalanceSheetGroup", type text},
        {"CashFlowCategory", type text},
        {"NormalBalance", type text},
        {"SortOrder", Int64.Type}
    })
in
    TypedTable
