// Dim_Entity.pq
// Ingests and types the multi-entity corporate structure master table.

let
    Source = Csv.Document(File.Contents("samples/sample-entities.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedTable = Table.TransformColumnTypes(PromoteHeaders, {
        {"EntityID", type text},
        {"LegalName", type text},
        {"TradingName", type text},
        {"ABN", type text},
        {"ACN", type text},
        {"TaxStructure", type text},
        {"EntityRole", type text},
        {"ANZSIC_Code", type text},
        {"Currency", type text},
        {"ConsolidationWeight", type number}
    })
in
    TypedTable
