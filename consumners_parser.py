import re
import json

def parse_new_csv_to_json(file_path):
    # Adjusted pattern to match the new structure, especially considering spaces in party names
    pattern = re.compile(r'^(\d+)\s+([\d\/A-Za-z]+)\s+(.+?)\s+(\*+\d+)\s+([A-Z]+)\s+(\d+)\s+([\d,]+)\s+(\d+)\s+(\d+)$')

    json_result = []

    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.match(line.strip())
            if not match:
                print(line)
                continue  # Skip lines that do not match the pattern

            sr_no, date_of_encashment, name_of_political_party, account_no, prefix, bond_number, denominations, pay_branch_code, pay_teller = match.groups()

            # Denominations should preserve commas for readability
            # Convert to integer if processing or calculations are needed

            json_result.append({
                "Sr No.": sr_no,
                "Date of Encashment": date_of_encashment,
                "Name of the Political Party": name_of_political_party.strip(),
                "Account no. of Political Party": account_no,
                "Prefix": prefix,
                "Bond Number": bond_number,
                "Denominations": denominations,  # Keep as string if commas are significant
                "Pay Branch Code": pay_branch_code,
                "Pay Teller": pay_teller
            })

    return json.dumps(json_result, indent=4)

file_path = 'consumers_data.txt'
json_output = parse_new_csv_to_json(file_path)
output_file_path = 'consumers_data.json'
with open(output_file_path, 'w') as f:
    f.write(json_output)
