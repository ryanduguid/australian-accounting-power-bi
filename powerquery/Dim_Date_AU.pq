// Dim_Date_AU.pq
// Generates an Australian Financial Year Date Dimension (1 July - 30 June)
// Parameters: StartDate (date), EndDate (date)

let
    GenerateDateDimension = (StartDate as date, EndDate as date) as table =>
    let
        DayCount = Duration.Days(EndDate - StartDate) + 1,
        DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
        TableFromList = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
        ChangedType = Table.TransformColumnTypes(TableFromList, {{"Date", type date}}),
        
        // Calendar attributes
        AddYear = Table.AddColumn(ChangedType, "CalendarYear", each Date.Year([Date]), Int64.Type),
        AddMonthNum = Table.AddColumn(AddYear, "MonthNumber", each Date.Month([Date]), Int64.Type),
        AddMonthName = Table.AddColumn(AddMonthNum, "MonthName", each Date.MonthName([Date]), type text),
        AddDay = Table.AddColumn(AddMonthName, "DayOfMonth", each Date.Day([Date]), Int64.Type),
        AddDayOfWeek = Table.AddColumn(AddDay, "DayOfWeek", each Date.DayOfWeek([Date], Day.Monday) + 1, Int64.Type),
        AddDayName = Table.AddColumn(AddDayOfWeek, "DayName", each Date.DayOfWeekName([Date]), type text),
        AddIsWeekend = Table.AddColumn(AddDayName, "IsWeekend", each if [DayOfWeek] >= 6 then true else false, type logical),
        
        // Australian Financial Year attributes (1 July to 30 June)
        AddFinYearNum = Table.AddColumn(AddIsWeekend, "FinancialYearNumber", each if [MonthNumber] >= 7 then [CalendarYear] + 1 else [CalendarYear], Int64.Type),
        AddFinYearLabel = Table.AddColumn(AddFinYearNum, "FinancialYear", each "FY" & Text.End(Text.From([FinancialYearNumber] - 1), 2) & "-" & Text.End(Text.From([FinancialYearNumber]), 2), type text),
        AddFinMonthNum = Table.AddColumn(AddFinYearLabel, "FinancialMonthNumber", each if [MonthNumber] >= 7 then [MonthNumber] - 6 else [MonthNumber] + 6, Int64.Type),
        AddFinQuarter = Table.AddColumn(AddFinMonthNum, "FinancialQuarter", each "FQ" & Text.From(Number.IntegerDivide([FinancialMonthNumber] - 1, 3) + 1), type text),
        AddFinYearQuarter = Table.AddColumn(AddFinQuarter, "FinancialYearQuarter", each [FinancialYear] & " " & [FinancialQuarter], type text),
        AddFinYearMonth = Table.AddColumn(AddFinYearQuarter, "FinancialYearMonth", each [FinancialYear] & "-" & Text.PadStart(Text.From([FinancialMonthNumber]), 2, "0"), type text),
        AddFYStartDate = Table.AddColumn(AddFinYearMonth, "FYStartDate", each #date([FinancialYearNumber] - 1, 7, 1), type date),
        AddFYEndDate = Table.AddColumn(AddFYStartDate, "FYEndDate", each #date([FinancialYearNumber], 6, 30), type date)
    in
        AddFYEndDate
in
    GenerateDateDimension
