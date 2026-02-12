# User Guide

Complete guide to using the Order Processing System.

## Table of Contents

- [Getting Started](#getting-started)
- [User Interface Overview](#user-interface-overview)
- [Uploading Files](#uploading-files)
- [Viewing Results](#viewing-results)
- [Managing History](#managing-history)
- [Understanding Reports](#understanding-reports)
- [Error Handling](#error-handling)
- [Tips and Best Practices](#tips-and-best-practices)
- [FAQ](#faq)

## Getting Started

### Accessing the Application

1. Ensure both backend and frontend servers are running
2. Open your web browser
3. Navigate to: http://localhost:8501

You should see the **Order Processing System** interface.

### First Time Users

1. Review the sample data: Open `sample_input.txt` in the project folder
2. Try processing the sample file to familiarize yourself with the interface
3. Check both the output report and error log views
4. Experiment with downloading results

## User Interface Overview

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Order Processing System                        [History] ▼  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Upload New Files                                           │
│  ┌────────────────────────────────┐                         │
│  │ Choose files               [Browse]  │                   │
│  └────────────────────────────────┘                         │
│                                                              │
│  Selected: orders.txt                                       │
│                                                              │
│  [Process Files]                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Main Components

1. **Sidebar (History)**
   - Lists previously processed submissions
   - Shows timestamp and file count
   - Expandable entries with View/Delete buttons

2. **Main Area**
   - File upload section (when no submission selected)
   - Results viewer (when submission selected)
   - Toggle between output and error views

3. **Action Buttons**
   - Process Files
   - Back to Upload
   - Download Report
   - Delete Submission

## Uploading Files

### Preparing Your Data

Your order file must be in **pipe-delimited format**:

```
OrderID|CustomerName|ProductName|Quantity|UnitPrice|OrderDate
```

**Example**:
```
ORD001|John Smith|Laptop|2|999.99|2024-03-15
ORD002|Jane Doe|Mouse|1|25.50|2024-03-16
ORD003|Bob Johnson|Keyboard|5|49.99|2024-03-17
```

### Field Requirements

| Field | Type | Format | Rules | Example |
|-------|------|--------|-------|---------|
| OrderID | Text | Any string | Required, unique | ORD001 |
| CustomerName | Text | Any string | Required, non-empty | John Smith |
| ProductName | Text | Any string | Required, non-empty | Laptop |
| Quantity | Integer | Whole number | Must be ≥ 0 | 2 |
| UnitPrice | Decimal | Number with decimals | Must be ≥ 0 | 999.99 |
| OrderDate | Date | YYYY-MM-DD | Valid date | 2024-03-15 |

### Upload Process

1. **Click "Choose files" button**
   - File browser opens
   - Only `.txt` files are selectable

2. **Select one or multiple files**
   - Hold Ctrl (Windows/Linux) or Cmd (Mac) for multiple selection
   - Files appear in the selected list

3. **Click "Process Files"**
   - Processing begins immediately
   - Spinner indicates progress
   - Success message appears when complete

4. **View Results**
   - Interface automatically switches to results view
   - Latest submission is displayed
   - Entry added to History sidebar

### Multiple File Upload

Process multiple files simultaneously:

```
Selected Files:
- orders_january.txt
- orders_february.txt  
- orders_march.txt

[Process Files]
```

**Benefits**:
- Faster batch processing
- Single submission record
- Compare results easily

## Viewing Results

### Submission View

After processing, you'll see:

```
┌─────────────────────────────────────────────────────────────┐
│  [← Back to Upload]    Submission: 2024-03-15 14:30         │
├─────────────────────────────────────────────────────────────┤
│  Select File: [orders.txt ▼]                                │
│                                                              │
│  View Mode: ⦿ Output Report  ○ Error Log                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Customer Name   │ Orders │ Items │ Gross │ Net      │  │
│  │  John Smith      │   3    │   4   │ $2.5K │ $2.3K   │  │
│  │  Jane Doe        │   2    │   3   │ $450  │ $450    │  │
│  │  ...                                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  [Download Output Report]                                   │
└─────────────────────────────────────────────────────────────┘
```

### Switching Between Files

If you uploaded multiple files:

1. Use the **"Select File"** dropdown
2. Choose the file you want to view
3. Results update automatically

### Toggle View Modes

**Output Report**:
- Customer summary table
- Order counts and totals
- Applied discounts
- Grand totals

**Error Log**:
- List of validation errors
- Problematic lines shown
- Error descriptions
- Empty if no errors

### Downloading Results

**Steps**:
1. Choose your desired view mode (Output or Error)
2. Click the **"Download"** button
3. File saves to your default download location
4. Filename includes the original name and type

**Downloaded Files**:
- `orders_output.txt` - Customer summary report
- `orders_error.txt` - Validation error log

## Managing History

### Viewing History

**Sidebar Display**:
```
History
───────────────────────────
▼ 2024-03-15 14:30 (3 files)
  [View Files]
  [Delete]
  
▼ 2024-03-15 10:15 (1 file)
  [View Files]
  [Delete]
```

**Information Shown**:
- Timestamp of processing
- Number of files in submission
- Expandable for actions

### Accessing Previous Submissions

1. **Click "View Files"** on any submission
2. Main area switches to that submission's results
3. Use file selector and view toggle as normal
4. Click **"Back to Upload"** when done

### Deleting Submissions

**Warning**: This action is permanent and cannot be undone.

**Steps**:
1. Locate submission in History sidebar
2. Expand the entry
3. Click **"Delete"** button
4. Confirmation message appears
5. Submission and all files removed

**What Gets Deleted**:
- Original uploaded file
- Generated output report
- Generated error log
- History record

## Understanding Reports

### Output Report Structure

```
+-----------------+----------+---------+---------------+------------+-------------+
|   Customer Name |   Orders |   Items |   Gross Total |   Discount |   Net Total |
+=================+==========+=========+===============+============+=============+
|      John Smith |        3 |       4 |     $2,529.97 |    $200.00 |   $2,329.97 |
+-----------------+----------+---------+---------------+------------+-------------+
|   Sarah Johnson |        3 |       6 |       $236.47 |      $0.00 |     $236.47 |
+-----------------+----------+---------+---------------+------------+-------------+
|     GRAND TOTAL |          |         |     $7,881.37 |    $589.89 |   $7,291.48 |
+-----------------+----------+---------+---------------+------------+-------------+
```

### Column Definitions

**Customer Name**: The customer who placed the orders

**Orders**: Total number of separate order lines for this customer
- Example: If John has ORD001, ORD002, ORD003, Orders = 3

**Items**: Total quantity of all items across all orders
- Example: 2 laptops + 1 monitor + 1 mouse = 4 items

**Gross Total**: Sum of all line totals before discounts
- Calculation: Σ(quantity × unit_price)

**Discount**: Total discount amount applied
- Rule: 10% discount on line items > $500
- Applied per order line, not per customer

**Net Total**: Final amount after discounts
- Calculation: Gross Total - Discount

### Business Rules

#### Discount Logic

Discount is applied **per order line**:

```
ORD001|John|Laptop|2|999.99|2024-03-15
Line Total: 2 × $999.99 = $1,999.98
Discount: $1,999.98 × 10% = $199.998 ≈ $200.00
Net: $1,999.98 - $200.00 = $1,799.98
```

**Important**: Discount threshold is per line, not per customer total.

```
Customer A:
- Order 1: $300 (no discount)
- Order 2: $600 (10% discount)
- Total discount: $60 (not $90)
```

### Grand Total

The **GRAND TOTAL** row shows:
- Sum of all Gross Totals across all customers
- Sum of all Discounts
- Sum of all Net Totals

## Error Handling

### Understanding Error Messages

**Invalid Quantity**:
```
Invalid quantity: -1. Must be non-negative. Line: ORD017|...|−1|...
```
- **Cause**: Negative quantity value
- **Fix**: Ensure quantity is 0 or positive

**Invalid Format**:
```
Invalid format: Expected 6 fields, got 5. Line: ORD018|...|75.00
```
- **Cause**: Missing field (likely date)
- **Fix**: Add all 6 required fields

**Invalid Date**:
```
Invalid date format: 23-03-2024. Expected YYYY-MM-DD. Line: ORD021|...|23-03-2024
```
- **Cause**: Wrong date format (DD-MM-YYYY instead of YYYY-MM-DD)
- **Fix**: Use YYYY-MM-DD format

**Invalid Price**:
```
Invalid unit price format: abc. Line: ORD022|...|abc|...
```
- **Cause**: Non-numeric price value
- **Fix**: Use numeric values (e.g., 99.99)

**Negative Price**:
```
Invalid unit price: -50.0. Must be non-negative. Line: ORD023|...|-50.00|...
```
- **Cause**: Negative price
- **Fix**: Use positive price values

### Error Recovery

**Partial Processing**:
The system processes all valid orders even if some lines have errors:

```
Input:
- 100 order lines
- 5 have errors
- 95 are valid

Output:
- Report contains 95 valid orders
- Error log lists 5 problematic lines
```

**Best Practice**:
1. Review error log
2. Fix problematic lines in source file
3. Re-upload corrected file
4. Verify all orders processed

### Common Mistakes

| Issue | Cause | Solution |
|-------|-------|----------|
| Missing data | Empty fields | Fill all 6 fields |
| Wrong separator | Comma instead of pipe | Use `|` character |
| Extra fields | Too many columns | Remove extra data |
| Date format | European format | Use YYYY-MM-DD |
| Decimal separator | Comma as decimal | Use period (.) |
| Line breaks | Extra blank lines | Remove empty lines |

## Tips and Best Practices

### Data Preparation

1. **Validate Before Upload**
   - Check file in text editor
   - Ensure consistent formatting
   - Verify date formats
   - Confirm 6 fields per line

2. **Use Consistent Naming**
   - Include date in filename: `orders_2024-03-15.txt`
   - Use descriptive names: `march_sales.txt`
   - Avoid special characters

3. **Batch Processing**
   - Group related files by time period
   - Upload multiple files together
   - Easier to compare results

### Working with Results

1. **Regular Downloads**
   - Download reports for record-keeping
   - Save error logs for data quality tracking
   - Archive monthly summaries

2. **Error Review**
   - Always check error log after processing
   - Fix issues in source data
   - Re-process corrected files

3. **History Management**
   - Delete old test submissions
   - Keep production runs
   - Name files clearly for easy identification

### Performance Tips

1. **File Size**
   - Optimal: < 10,000 orders per file
   - Large files: May take longer to process
   - Consider splitting very large datasets

2. **Browser Performance**
   - Close unused tabs
   - Refresh page if slow
   - Use modern browser versions

## FAQ

### General Questions

**Q: What file formats are supported?**
A: Only `.txt` files with pipe-delimited data are supported.

**Q: Is there a file size limit?**
A: Currently no hard limit, but files under 5MB process fastest.

**Q: Can I upload Excel or CSV files?**
A: Not directly. Convert to pipe-delimited `.txt` format first.

**Q: How long is history kept?**
A: History persists until manually deleted or server storage is cleared.

### Data Questions

**Q: Can customer names have special characters?**
A: Yes, but avoid using pipe `|` character as it's the delimiter.

**Q: What if two customers have the same name?**
A: They're treated as the same customer in the report.

**Q: Can I have multiple orders with the same Order ID?**
A: Yes, but it's not recommended. Each line is processed independently.

**Q: What date range is valid?**
A: Any valid date in YYYY-MM-DD format. No specific range restrictions.

### Processing Questions

**Q: What happens if one line has errors?**
A: That line is logged in the error file, but other valid lines are still processed.

**Q: Is the discount cumulative?**
A: No, it's applied per order line, not per customer total.

**Q: Can I change the discount percentage?**
A: Not in the current version. Contact support for customization.

**Q: How are ties handled in the report?**
A: Customers are listed in the order they appear in the file.

### Technical Questions

**Q: Where is my data stored?**
A: Locally on the server in the `backend/data/` directory.

**Q: Is my data secure?**
A: Data is stored locally. For production use, implement authentication.

**Q: Can multiple users upload simultaneously?**
A: Yes, but each submission is processed independently.

**Q: How do I backup my data?**
A: Copy the entire `backend/data/` directory.

### Troubleshooting

**Q: The page won't load**
A: Ensure both backend and frontend servers are running.

**Q: Upload button does nothing**
A: Check browser console for errors. Try refreshing the page.

**Q: Download button not working**
A: Ensure the file was processed successfully. Check the error log.

**Q: Previous submissions disappeared**
A: Check if `history.json` was deleted or corrupted.

## Getting Help

**Documentation**:
- [Quick Start Guide](QUICKSTART.md) - Setup instructions
- [API Documentation](API.md) - API reference
- [Architecture Guide](ARCHITECTURE.md) - System design

**Support Channels**:
- GitHub Issues: For bugs and feature requests
- Discussions: For questions and help
- Email: support@example.com (if configured)

**Reporting Issues**:
When reporting a problem, include:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Screenshot (if UI issue)
5. Sample data (if data issue)

---

**Need more help?** Check our [troubleshooting guide](QUICKSTART.md#common-issues) or open an issue on GitHub.
