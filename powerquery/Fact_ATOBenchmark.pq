// Fact_ATOBenchmark.pq
// Ingests ATO Small Business Benchmarks across industry codes (ANZSIC) and turnover brackets.

let
    Source = Csv.Document(File.Contents("samples/sample-ato-benchmarks.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedTable = Table.TransformColumnTypes(PromoteHeaders, {
        {"ANZSIC_Code", type text},
        {"TurnoverRange", type text},
        {"GrossProfitPct_Low", type number},
        {"GrossProfitPct_Avg", type number},
        {"GrossProfitPct_High", type number},
        {"TotalExpensesPct_Avg", type number},
        {"RentPct_Avg", type number},
        {"MotorVehiclePct_Avg", type number},
        {"LabourPct_Avg", type number}
    })
in
    TypedTable
