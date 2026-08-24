// Fx_ValidateABN.pq
// Validates an Australian Business Number (ABN) using the statutory ATO Modulus-89 algorithm.
// Algorithm:
// 1. Subtract 1 from the first digit.
// 2. Multiply each of the 11 digits by its assigned weighting: [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19].
// 3. Sum the resulting products.
// 4. Divide sum by 89. If remainder is 0, the ABN checksum is valid.

let
    ValidateABN = (abnInput as any) as logical =>
    let
        RawText = Text.Select(Text.From(abnInput), {"0".."9"}),
        Weights = {10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19},
        IsValid = if Text.Length(RawText) <> 11 then
            false
        else
            let
                Digits = List.Transform(Text.ToList(RawText), each Number.FromText(_)),
                AdjustedFirst = {Digits{0} - 1} & List.Skip(Digits, 1),
                Products = List.Zip({AdjustedFirst, Weights}),
                WeightedSum = List.Sum(List.Transform(Products, each _{0} * _{1})),
                Remainder = Number.Mod(WeightedSum, 89)
            in
                (Remainder = 0)
    in
        IsValid
in
    ValidateABN
