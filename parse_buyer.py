import re
import json

def parse_custom_csv_to_json(file_path):
    # Improved pattern to match starting and ending fields more reliably
    pattern = re.compile(r'^(\d+)\s+(\d+)\s+([\d\/A-Za-z]+)\s+([\d\/A-Za-z]+)\s+([\d\/A-Za-z]+)\s+(.+)\s+([A-Z]+)\s+(\d+)\s+([\d,]+)\s+(\d+)\s+(\d+)\s+(\w+)$')
    json_result = []

    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.match(line.strip())
            if not match:
                print(line)
                continue

            sr_no, reference_no, journal_date, date_of_purchase, date_of_expiry, middle_section, prefix, bond_number, denominations, issue_branch_code, issue_teller, status = match.groups()

            # Handle the 'Denominations' field specifically to remove commas and convert to integer
            denominations = denominations.replace(',', '')  # Remove commas
            # Ensure 'Denominations' is a valid integer
            
            
            # Process 'middle_section' to extract the name, accounting for its variability
            # This example assumes 'middle_section' ends with the name, which may need adjustment
            name_of_purchaser = middle_section

            json_result.append({
                "Sr No.": sr_no,
                "Reference No (URN)": reference_no,
                "Journal Date": journal_date,
                "Date of Purchase": date_of_purchase,
                "Date of Expiry": date_of_expiry,
                "Name of the Purchaser": name_of_purchaser,
                "Prefix": prefix,
                "Bond Number": bond_number,
                "Denominations": int(denominations),
                "Issue Branch Code": issue_branch_code,
                "Issue Teller": issue_teller,
                "Status": status
            })

    return json.dumps(json_result, indent=4)


file_path = 'buyers_data.txt'
json_output = parse_custom_csv_to_json(file_path)
output_file_path = 'buyers_data.json'
with open(output_file_path, 'w') as f:
    f.write(json_output)