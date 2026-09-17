
    
    use calamine::{open_workbook, Reader, Xlsx};
    // Open the workbook (use Xlsx for .xlsx, or open_workbook_auto for auto-detection)
    let mut excel: Xlsx<_> = open_workbook("keywords.xlsx")?;
    // Get the first sheet name
    let sheet_name = excel.sheet_names().first().cloned()
        .ok_or_else(|| calamine::Error::Msg("No sheets found in the Excel file".into()))?;

    // Read the worksheet
    let range = excel.worksheet_range(&sheet_name)?;

    // Vector to store the first column strings
    let mut first_column_strings: Vec<String> = Vec::new();

    // Iterate through the rows of the worksheet
    for row in range.rows() {
        // Check if the row has at least one cell (the first column)
        if let Some(cell) = row.first() {
            // Convert the cell value to a String and push it to the vector
            first_column_strings.push(cell.to_string());
        }
    }

    // Print the results to verify
    println!("First column values: {:#?}", first_column_strings);

    Ok(())
}