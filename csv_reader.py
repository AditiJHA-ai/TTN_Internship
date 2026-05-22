import csv
import os
 
SAMPLE_CSV = "sample_data.csv"
 
def create_sample_csv():
    """Creates a sample CSV file for demonstration."""
    rows = [
        ["Name", "Age", "Department", "Salary"],
        ["Alice", "30", "Engineering", "90000"],
        ["Bob", "25", "Marketing", "65000"],
        ["Charlie", "35", "Engineering", "105000"],
        ["Diana", "28", "HR", "70000"],
        ["Eve", "32", "Marketing", "72000"],
    ]
    with open(SAMPLE_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Sample CSV created: {SAMPLE_CSV}")
 
def read_csv(filepath):
    """Reads and returns all rows from a CSV file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
 
    rows = []
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows
 
def display_rows(rows):
    """Prints rows in a simple table format."""
    if not rows:
        print("No data found.")
        return
    headers = list(rows[0].keys())
    col_widths = {h: max(len(h), max(len(r[h]) for r in rows)) for h in headers}
    header_line = "  ".join(h.ljust(col_widths[h]) for h in headers)
    print(header_line)
    print("-" * len(header_line))
    for row in rows:
        print("  ".join(row[h].ljust(col_widths[h]) for h in headers))
 
def filter_by_department(rows, department):
    """Returns rows matching the given department."""
    return [r for r in rows if r.get("Department", "").lower() == department.lower()]
 
if __name__ == "__main__":
    create_sample_csv()
    try:
        data = read_csv(SAMPLE_CSV)
        print(f"\nAll records ({len(data)} total):")
        display_rows(data)
 
        dept = "Engineering"
        filtered = filter_by_department(data, dept)
        print(f"\nFiltered by department '{dept}':")
        display_rows(filtered)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
