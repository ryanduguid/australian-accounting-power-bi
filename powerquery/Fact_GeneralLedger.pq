// Fact_GeneralLedger.pq
// Ingests, validates, and types balanced General Ledger journal entries.

let
    Source = Csv.Document(File.Contents("samples/sample-general-ledger.csv"), [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedTable = Table.TransformColumnTypes(PromoteHeaders, {
        {"JournalID", type text},
        {"LineNumber", Int64.Type},
        {"PostingDate", type date},
        {"EntityID", type text},
        {"AccountCode", type text},
        {"Debit", type number},
        {"Credit", type number},
        {"Amount", type number},
        {"Description", type text},
        {"IntercompanyEntityID", type text},
        {"IsIntercompany", type logical}
    })
in
    TypedTable
